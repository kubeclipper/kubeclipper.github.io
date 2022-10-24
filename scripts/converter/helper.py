import os
import re


META_SEP = '---'

SCOPE_REG = re.compile(r'^docscope: (\w+)')


def find_meta_index(lst, value):
    ret = []
    idx = 0
    for line in lst:
        if value == line.strip():
            ret.append(idx)
        idx = idx + 1
    return ret


def is_markdown(filename):
    if os.path.basename(filename).endswith(".md"):
        return True
    return False


def is_image(filename):
    for img in ['.png', '.jpg', '.gif', '.svg']:
        if os.path.basename(filename).endswith(img):
            return True
    return False


def is_index_markdown(filename):
    if os.path.basename(filename) == '_index.md':
        return True
    return False


def get_markdown_metadata(filename):
    if not is_markdown(filename):
        raise Exception("file %s is not markdown" % filename)
    try:
        with open(filename) as f:
            return get_markdown_content_metadata(f.read())
    except Exception as e:
        raise Exception("get file %s meta: %s" % (filename, e))


def get_markdown_content_metadata(content):
    import yaml
    contents = content.splitlines()
    idxs = find_meta_index(contents, META_SEP)
    if len(idxs) < 2:
        raise Exception("Not found paired %s in contents, index is %s" % (META_SEP, len(idxs)))
    meta_lines = contents[idxs[0]+1:idxs[1]]
    meta = yaml.load('\n'.join(meta_lines), Loader=yaml.FullLoader)
    return meta


def copy_file(src, to):
    import shutil
    target_dir = os.path.dirname(to)
    makedirs(target_dir)
    shutil.copy2(src, to)
    # print("copy %s to %s" % (src, to))


def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == '__main__':
    meta = get_markdown_content_metadata('''
---
k1: v1
k2: v2
k3:
- 1
- 2
- 3
k4:
  v1:
    v2: 123
---
---
    ''')
    print("%s" % meta)
