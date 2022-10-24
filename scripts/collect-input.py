#!/usr/bin/env python3


import sys
import os
import os.path
import yaml
import subprocess
import glob
import re

from typing import List, Union, Mapping

from converter import *


def ls_cmd_num_str(num: int) -> str:
    num_str = str(num)
    if len(num_str) == 1:
        return "0" + num_str
    return num_str


def get_output_meta_file(target_dir):
    return os.path.join(target_dir, OUTPUT_META_BASEFILE)


class SingleMDFile(object):

    CODE_SEP = '~~~'
    META_SEP = META_SEP

    def __init__(self, inside_dir, input_file: str, is_index: bool=False):
        self.inside_dir: MDDir = inside_dir
        self.meta: Union[Mapping, None] = None
        self.is_index = is_index
        self.title: str = ""
        self.weight: Union[int, None] = None
        self.description: str = ""
        self.content: str = ""
        self.input_file: str = input_file

    def parse_file(self):
        print("[start] parse file %s" % self.input_file)
        self.__parse_file()
        print("[end] md file %s" % self.get_output_filename())
        return self

    def get_depth(self):
        if self.is_index:
            return self.inside_dir.depth
        return self.inside_dir.depth + 1

    def get_output_weight(self) -> int:
        if self.is_index:
            return 0
        return self.weight + 1

    def __parse_file(self):
        with open(self.input_file) as f:
            contents = f.readlines()
            self.__parse_content(contents)

    def __parse_content(self, contents):
        if len(contents) == 0:
            return
        idxs = find_meta_index(contents, META_SEP)
        if len(idxs) == 0:
            self.set_content(contents)
            return
        if len(idxs) < 2:
            raise Exception("Not found paired %s in contents, index is %s" % (self.META_SEP, len(idxs)))
        meta_lines = contents[idxs[0]+1:idxs[1]]
        self.meta = yaml.load(''.join(meta_lines), Loader=yaml.FullLoader)
        self.title = self.meta.get('title', '')
        self.weight = self.meta.get('weight', MD_MAX_WEIGHT)
        self.description = self.meta.get('description', '')
        self.set_content(contents[idxs[1]+1:])

    def set_content(self, lines):
        out_meta = {
                "input_file": self.input_file,
                "header_level": self.get_depth(),
                "meta_title": self.title,
                "description": self.description,
                "images_path": self.inside_dir.get_md_output_image_dirname(),
        }
        yaml_str = yaml.dump(out_meta, allow_unicode=True)
        meta_sep = self.META_SEP + '\n'
        meta_lines = [meta_sep, yaml_str, meta_sep]
        #meta_sep = self.CODE_SEP + ' ocmeta\n'
        #meta_lines = [meta_sep, yaml_str, self.CODE_SEP+'\n']
#         lines = [self.replace_line_var(l) for l in lines]
        self.content = ''.join(meta_lines + lines)

#     def replace_line_var(self, line: str):
#         VAR_OEM_NAME = 'var_oem_name'
#         VAR_CT_OEM_NAME = '{{<oem_name>}}'
#         ALERT_REG_START = re.compile(r'(\s*){{.*alert\s.*title="(.*?)".*}}')
#         ALERT_REG_END = re.compile(r'(\s*){{%.*/alert.*%}}')
#         for placeholder in [VAR_OEM_NAME, VAR_CT_OEM_NAME]:
#             if placeholder in line:
#                 line = line.replace(placeholder, get_oem_name(), -1)
#         m_s = ALERT_REG_START.match(line)
#         m_e = ALERT_REG_END.match(line)
#         if m_s is not None:
#             #import ipdb; ipdb.set_trace()
#             white_space = m_s.groups()[0]
#             title = m_s.groups()[1]
#             line = "%s**%s:**" % (white_space, title)
#         elif m_e is not None:
#             line = m_e.groups()[0]
#         return line

    def get_output_filename(self):
        basename = os.path.basename(self.input_file)
        if self.inside_dir is None:
            return basename
        inside_dir_name = self.inside_dir.get_ouput_prefix()
        if self.weight is None:
            return inside_dir_name + basename
        weight_str = ls_cmd_num_str(self.get_output_weight())
        return inside_dir_name + "%s-%s" % (weight_str, basename)

    def get_output_path(self, target_dir):
        basename = self.get_output_filename()
        def concat_dir(basename):
            return os.path.join(target_dir, basename)
        return concat_dir(basename)

    def get_output_content(self):
        return self.content

    def call_pandoc(self, target_dir, outpath):
        env = os.environ.copy()
        env[OUTPUT_META_BASEFILE_KEY] = get_output_meta_file(target_dir)
        process = subprocess.Popen([
            "pandoc", "-f", "markdown-markdown_in_html_blocks+raw_html",
            "--lua-filter", "./pandoc-table-filter.lua",
            "--filter", "./pandoc-doc-filter.py",
            "-t", "markdown", outpath, "-o", outpath], env=env)
        process.wait()

    def output(self, target_dir):
        outpath = self.get_output_path(target_dir)
        dirname = os.path.dirname(outpath)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(outpath, 'w') as f:
            f.write(self.get_output_content())
        self.call_pandoc(target_dir, outpath)


class MDDir(object):

    INDEX_MD = "_index.md"

    def __init__(self, dirname: str, parent_dir=None, output_parts: List[str]=[]):
        self.dirname: str = dirname
        self.name: str = os.path.basename(dirname)
        if parent_dir is not None and len(output_parts):
            raise Exception("only root dir can export parts directory")
        self.export_parts = output_parts
        self.part_export = False
        self.parent_dir: Union[MDDir, None] = parent_dir
        self.images_dir: str = ""
        self.child_dirs: List[MDDir] = []
        self.index_md: Union[SingleMDFile, None] = None
        self.depth: Union[int, None] = None
        self.md_files: List[SingleMDFile] = []

    def set_part_export(self, part_export):
        self.part_export = part_export

    def start_init(self):
        self.init_images_dir()
        self.init_depth(self.parent_dir)
        self.__construct()
        return self

    def init_images_dir(self):
        found_records = {}
        for imgs_dir in ["images", "image"]:
            full_dir = os.path.join(os.path.realpath(self.dirname), imgs_dir)
            if not os.path.exists(full_dir):
                continue
            found_records[imgs_dir] = full_dir
        if len(found_records) > 0 and len(found_records) != 1:
            raise Exception("Duplicate image dir %s inside %s" % (found_records.values(), self.dirname))
        def dir_contains_png(check_dir):
            items = glob.glob(os.path.join(check_dir, "*.png"))
            items = items + glob.glob(os.path.join(check_dir, "**", "*.png"))
            for item in items:
                if item.endswith(".png"):
                    return True
            return False
        for k in found_records.keys():
            check_dir = found_records[k]
            if dir_contains_png(check_dir):
                self.images_dir = found_records[k]
                break

    def is_root_dir(self):
        if self.parent_dir is None:
            return True
        return False

    def should_export(self):
        # full export condition
        if self.is_root_dir():
            if len(self.export_parts) == 0:
                return True
            return False
        if self.part_export:
            return True
        return self.parent_dir.should_export()

    def init_depth(self, parent_dir):
        if parent_dir is None or self.part_export:
            self.depth = 1
            return
        self.depth = self.parent_dir.depth + 1

    def get_index_weight(self):
        if self.is_root_dir():
            return MD_MIN_WEIGHT
        if self.index_md is None:
            return MD_MAX_WEIGHT
        return self.index_md.weight

    def get_output_index_weight(self) -> str:
        if self.is_root_dir():
            raise Exception("root dir %s get_output_index_weight should not invoked" % self.name)
        return ls_cmd_num_str(self.get_index_weight() + 1)

    #  def get_out_weight_prefix(self):
        #  depth_str = ls_cmd_num_str(self.depth)
        #  weight_str = ls_cmd_num_str(self.get_index_weight())
        #  if self.is_root_dir():
            #  return depth_str + "_"
        #  return depth_str + "_" + weight_str + "_"

    def get_parenet_output_prefix(self):
        if self.is_root_dir():
            return self.name + "_"
        return self.parent_dir.get_parenet_output_prefix() + \
                self.get_output_index_weight() + "_" + self.name + "_"

    def get_ouput_prefix(self):
        prefix = self.get_parenet_output_prefix()
        return prefix
        #  if self.is_root_dir():
            #  return prefix
        #  return prefix + ls_cmd_num_str(self.get_index_weight())

    def get_output_image_dirname(self):
        if self.images_dir == "":
            return None
        return self.get_ouput_prefix() + os.path.basename(self.images_dir)

    def get_md_output_image_dirname(self):
        if self.is_root_dir():
            if self.images_dir == "":
                return IMAGE_DIR_NOT_PROVIDED
            return self.get_output_image_dirname()
        if self.images_dir == "":
            return self.parent_dir.get_md_output_image_dirname()
        return self.get_output_image_dirname()

    def __construct(self):
        index_md_path = os.path.join(self.dirname, self.INDEX_MD)
        if not os.path.exists(index_md_path):
            raise Exception("dir %s not contains index md %s" % (self.dirname, INDEX_MD))
        self.parse_index()
        for (dirpath, dirnames, filenames) in os.walk(self.dirname):
            self.__construct_child_dirs(dirnames)
            self.__construct_md_files(filenames)
            break

    def parse_index(self):
        index_md_path = os.path.join(self.dirname, self.INDEX_MD)
        md_obj = SingleMDFile(self, index_md_path, is_index=True)
        self.index_md = md_obj
        self.index_md.parse_file()
        # _index.md always is first item in self.md_files
        self.md_files = [self.index_md]

    def __construct_child_dirs(self, dirnames):

        def cons_child_dir(subdirname):
            subdir = os.path.join(self.dirname, subdirname)
            subpath = os.path.join(subdir, self.INDEX_MD)
            if not os.path.exists(subpath):
                return
            child_dir = MDDir(subdir, self)
            if len(self.export_parts) != 0 and child_dir.name in self.export_parts:
                child_dir.set_part_export(True)
            child_dir.start_init()
            self.child_dirs.append(child_dir)

        for dirname in dirnames:
            cons_child_dir(dirname)

    def __construct_md_files(self, filenames):
        md_files = [x for x in filenames if x.endswith(".md")]

        def cons_md_file(filename):
            if self.INDEX_MD in filename:
                return None
            fullpath = os.path.join(self.dirname, filename)
            obj = SingleMDFile(self, fullpath)
            return obj.parse_file()
        for filename in md_files:
            md_obj = cons_md_file(filename)
            if md_obj is None:
                continue
            self.md_files.append(md_obj)

    def ensure_output_meta_file(self, target_dir):
        filename = get_output_meta_file(target_dir)
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write(yaml.dump({"__meta_file__": filename}))
        return filename

    def get_output_meta(self, target_dir):
        filename = self.ensure_output_meta_file(target_dir)
        meta = {}
        with open(filename) as f:
            obj = yaml.load(f, Loader=yaml.FullLoader)
            if obj is not None:
                meta = obj
        return meta

    def save_output_meta(self, target_dir, meta):
        filename = get_output_meta_file(target_dir)
        with open(filename, "w") as f:
            yaml_str = yaml.dump(meta, allow_unicode=True)
            f.write(yaml_str)

    def output_link_images_dir(self, target_dir):
        for child in self.child_dirs:
            child.output_link_images_dir(target_dir)
        if self.images_dir != "":
            image_dirname = self.get_output_image_dirname()
            output_images_dir = os.path.join(target_dir, image_dirname)
            os.symlink(self.images_dir, output_images_dir)
            outmeta = self.get_output_meta(target_dir)
            img_meta = outmeta.get("images", {})
            img_meta[image_dirname] = self.images_dir
            outmeta["images"] = img_meta
            self.save_output_meta(target_dir, outmeta)

    def output_mds(self, target_dir):
        # output sub MDDir
        for child in self.child_dirs:
            child.output_mds(target_dir)
        if not self.should_export():
            return
        # output inside markdown files
        for md in self.md_files:
            md.output(target_dir)

    def output(self, target_dir):
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        self.output_link_images_dir(target_dir)
        self.output_mds(target_dir)

def show_help(progname):
    help_content = """
usage: %s <input_dir> <output_dir>
    """ % progname
    print(help_content)


if __name__ == '__main__':
    args = sys.argv
    progname = args[0]
    if len(args) < 3:
        show_help(progname)
        sys.exit(1)
    input_dir = args[1]
    output_dir = args[2]
    output_parts = []
    if len(args) > 3:
        output_parts = args[3:]
    obj = MDDir(input_dir, output_parts=output_parts).start_init()
    obj.output(output_dir)
