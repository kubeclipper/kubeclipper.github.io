import os
import tempfile

from utils import run_process


class Hugo(object):

    def __init__(self, content_dir):
        self._host = ''
        self._base_config = 'config.toml'
        self._title = 'KubeClipper'
        self._content_dir = content_dir
        self._base_url_prefix = ''
        self._dest_dir = 'public'
        self._current_branch = ''
        self._current_version = ''
        self._versions = []

    def set_base_config(self, filename):
        self._base_config = filename

    def set_host(self, host):
        self._host = host
        return self

    def get_host(self):
        return self._host

    def get_title(self):
        return self._title

    def set_title(self, title):
        self._title = title
        return self

    def set_current_branch(self, cur_br):
        self._current_branch = cur_br
        return self

    def get_current_branch(self):
        return self._current_branch

    def set_current_version(self, ver):
        self._current_version = ver
        return self

    def get_current_version(self):
        return self._current_version

    def set_versions(self, versions):
        self._versions = versions
        return self

    def set_base_url_prefix(self, pre):
        self._base_url_prefix = pre
        return self

    def get_base_url_prefix(self):
        return self._base_url_prefix

    def set_dest_dir(self, dest):
        self._dest_dir = dest
        return self

    def get_dest_dir(self):
        return self._dest_dir

    def generate_config_toml(self):
        config_content = '''contentDir = "%s"\n''' % (self._content_dir)
        config_content += '''
[languages]
[languages.zh-cn]
contentDir = "%s"\n''' % (os.path.join(self._content_dir, 'zh-cn'))
        
        config_content += '''\n
[languages.en]
contentDir = "%s"\n''' % (os.path.join(self._content_dir, 'en'))

        fp = tempfile.NamedTemporaryFile(delete=False, prefix='kubeclipper-docs', suffix='.toml')
        fp.write(config_content.encode(encoding='utf-8'))
        return fp.name

    def execute(self):
        env = {}
        env['CONTENT_DIR'] = self._content_dir

        if self.get_current_branch():
            env['CURRENT_BRANCH'] = self.get_current_branch()
        if self.get_current_version():
            env['CURRENT_VERSION'] = self.get_current_version()
        if self._versions:
            env['VERSIONS'] = ','.join(['v'+v for v in self._versions])

        ver_dir = ''
        ver_title = self.get_title()
        if self._versions:
            if not self.get_current_version():
                raise Exception("Current version not set when versions are %s" % self._versions)
            if self.get_current_version() != self._versions[0]:
                ver_dir = 'v' + self.get_current_version()
                ver_title = ver_title + ' ' + self.get_current_version()

        env['HUGO_TITLE'] = ver_title


        dest = self.get_dest_dir()
        base_url = self.get_host()
        base_url = os.path.join(base_url, self.get_base_url_prefix())
        if not base_url.endswith("/"):
            base_url += "/"
        if ver_dir:
            dest = os.path.join(dest, ver_dir)
            base_url = base_url + '/' + ver_dir

        temp_config_file = self.generate_config_toml()
        cmd = ['hugo',
               '--minify',
               '--config=%s,%s' % (self._base_config, temp_config_file),
               '--contentDir=%s' % self._content_dir,
               '--destination=%s' % dest,
               '--baseURL=%s' % base_url]
        run_process(['rm', '-rf', dest])
        run_process(cmd, env)
        print("=== Build result: %s" % dest)
