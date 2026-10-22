import json
import os
import tempfile

from utils import run_process


class Hugo(object):

    def __init__(self, content_dir):
        self._host = ''
        self._base_config = 'config.toml'
        self._content_dir = content_dir
        self._base_url_prefix = ''
        self._dest_dir = 'public'
        self._current_version = ''
        self._versions = []
        self._version_path = ''
        self._static_dir = 'static'
        self._github_subdir = ''

    def set_base_config(self, filename):
        self._base_config = filename

    def set_host(self, host):
        self._host = host

    def set_current_version(self, version):
        self._current_version = version

    def set_versions(self, versions):
        self._versions = versions

    def set_version_path(self, path):
        self._version_path = path

    def set_static_dir(self, path):
        self._static_dir = path

    def set_github_subdir(self, path):
        self._github_subdir = path

    def set_base_url_prefix(self, prefix):
        self._base_url_prefix = prefix

    def set_dest_dir(self, dest):
        self._dest_dir = dest

    def generate_config_toml(self):
        quote = json.dumps
        latest = self._versions[0] if self._versions else self._current_version
        archived = self._current_version != latest
        lines = [
            'contentDir = ' + quote(os.path.abspath(self._content_dir)),
            'staticDir = [' + quote(os.path.abspath(self._static_dir)) + ']',
            'canonifyURLs = true',
            '[languages.zh-cn]',
            'contentDir = ' + quote(os.path.abspath(os.path.join(self._content_dir, 'zh-cn'))),
            '[languages.en]',
            'contentDir = ' + quote(os.path.abspath(os.path.join(self._content_dir, 'en'))),
            '[params]',
            'version = ' + quote(self._current_version),
            'archived_version = ' + str(archived).lower(),
            'url_latest_version = ' + quote(self._host.rstrip('/') + '/'),
            'github_branch = ' + quote('release/' + self._current_version if archived and not self._github_subdir else 'master'),
            'github_subdir = ' + quote(self._github_subdir),
        ]
        if self._versions:
            lines += [
                '[[params.versions]]',
                'version = ' + quote('v' + latest + ' (latest)'),
                'url = ' + quote(self._host.rstrip('/') + '/'),
            ]
            for version in self._versions:
                lines += [
                    '[[params.versions]]',
                    'version = ' + quote('v' + version),
                    'url = ' + quote(self._host.rstrip('/') + '/v' + version + '/'),
                ]
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False,
                                         prefix='kubeclipper-docs-', suffix='.toml') as fp:
            fp.write('\n'.join(lines) + '\n')
            return fp.name

    def execute(self):
        dest = os.path.join(self._dest_dir, self._version_path)
        prefix = '/'.join(part.strip('/') for part in
                          [self._base_url_prefix, self._version_path] if part.strip('/'))
        base_url = self._host.rstrip('/') + '/' + (prefix + '/' if prefix else '')
        config_file = self.generate_config_toml()
        try:
            run_process(['rm', '-rf', dest])
            run_process([
                'hugo', '--minify',
                '--config=' + self._base_config + ',' + config_file,
                '--destination=' + dest,
                '--baseURL=' + base_url,
            ])
        finally:
            os.unlink(config_file)
        print('=== Build result: ' + dest)
