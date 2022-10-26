#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from . import helper


META_KEY_DOCSCOPE = 'docscope'
SCOPE_SYSTEM = 'system'
SCOPE_DOMAIN = 'domain'
SCOPE_PROJECT = 'project'
ALL_SCOPES = [SCOPE_SYSTEM, SCOPE_DOMAIN, SCOPE_PROJECT]

META_KEY_EDITION = 'edition'
EDITION_EE = 'ee'
EDITION_CE = 'ce'

META_KEY_EDITION = 'edition'
META_VAL_EDITION_CE = 'ce'
META_VAL_EDITION_EE = 'ee'


def add_skip_dir(skip_dirs, dirpath, subdirs):
    print("skip dir %s: %s" % (dirpath, subdirs))
    skip_dirs.append(dirpath)
    for subdir in subdirs:
        # do not skip image and images subdir
        if subdir in ["image", "images"]:
            continue
        fullpath = os.path.join(dirpath, subdir)
        skip_dirs.append(fullpath)
    return skip_dirs


class DirProcess(object):

    def __init__(self, src_dir, dest_dir):
        self._src_dir = src_dir
        self._dest_dir = dest_dir

        # include condition
        self._include_funcs = []

    def append_func(self, f):
        self._include_funcs.append(f)
        return self

    def include_by_scope(self, input_scope):
        def f(filepath, meta):
            return _include_by_scope(filepath, meta, input_scope)
        return self.append_func(f)

    def include_by_edition(self, edition):
        def f(fp, meta):
            return _include_by_edition(fp, meta, edition)
        return self.append_func(f)

    def _new_file_processor(self, dirpath, filename):
        fp = FileProcessor(dirpath, filename, self._dest_dir)
        return fp.set_include_funcs(self._include_funcs)

    def start(self):
        helper.makedirs(self._dest_dir)
        skip_dirs = []
        for (dirpath, dirnames, filenames) in os.walk(self._src_dir):
            # check parent dir in skip_dirs
            for p_dir in skip_dirs:
                if p_dir in dirpath:
                    skip_dirs.append(dirpath)
                    break

            if dirpath in skip_dirs:
                continue

            if self.should_skip_dir(dirpath, filenames):
                skip_dirs = add_skip_dir(skip_dirs, dirpath, dirnames)
                continue

            for filename in filenames:
                fp = self._new_file_processor(dirpath, filename)
                fp.start()

    def should_skip_dir(self, dirpath, filenames):
        idx_md = '_index.md'
        if idx_md not in filenames:
            return False
        fp = self._new_file_processor(dirpath, idx_md)
        return not fp.should_include()


class FileProcessor(object):

    def __init__(self, dirpath, filename, output_dir):
        self.dirpath = dirpath
        self.fullpath = os.path.join(dirpath, filename)
        self.output_dir = output_dir
        self._include_funcs = []

    def _is_image(self):
        return helper.is_image(self.fullpath)

    def is_markdown(self):
        return helper.is_markdown(self.fullpath)

    def _copy_to_dest(self):
        subpath_segs = os.path.normpath(self.fullpath).split(os.sep)[1:]
        subpath = os.path.join(*subpath_segs)
        topath = os.path.join(self.output_dir, subpath)
        helper.copy_file(self.fullpath, topath)

    def set_include_funcs(self, fs):
        self._include_funcs = fs
        return self

    def should_include(self):
        for include_f in self._include_funcs:
            try:
                if not include_f(self.fullpath,
                                helper.get_markdown_metadata(self.fullpath)):
                    # skip copy this file
                    print("skip file %s" % self.fullpath)
                    return False
            except Exception as e:
                raise Exception("%s: %s" % (self.fullpath, e))
        return True

    def start(self):
        if not self.is_markdown():
            # just copy to destination
            self._copy_to_dest()
            return

        if not self.should_include():
            return

        self._copy_to_dest()


def _include_by_scope(filepath, meta, input_scope):
    def is_less_than(s1, s2):
        smap = {
            SCOPE_SYSTEM: 3,
            SCOPE_DOMAIN: 2,
            SCOPE_PROJECT: 1,
        }
        ss1 = smap[s1]
        ss2 = smap[s2]
        return ss1 <= ss2


    # if file_scope is less or equal than input require scope
    # file should included
    # e.g. project < domain, domain < system
    file_scope = meta.get(META_KEY_DOCSCOPE, SCOPE_PROJECT)
    if file_scope not in ALL_SCOPES:
        raise Exception('%s: invalid scope %s' % (filepath, file_scope))
    if is_less_than(file_scope, input_scope):
        return True
    return False

def _include_by_edition(filepath, meta, input_edition):
    edition = meta.get(META_KEY_EDITION, None)
    if edition and edition != input_edition:
        print("%s: ignored by edition %s != %s" % (filepath, edition, input_edition))
        return False
    return True
