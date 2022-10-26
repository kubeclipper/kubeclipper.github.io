import os

from .consts import MODE_ONLINE, MODE_OFFLINE
from .consts import VERSION_ARRAY
from .hugo import Hugo
from utils import run_process
from converter import processor


__drivers = {}


def __register_driver(mode, drv):
    __drivers[mode] = drv


def get_driver(mode):
    drv = __drivers.get(mode, None)
    if drv:
        return drv
    raise Exception('Not found driver by mode: %s' % mode)


class BaseDriver(object):

    def __init__(self, mode):
        self._mode = mode

    def get_mode(self):
        return self._mode

    def get_scopes(self):
        return [
            [processor.SCOPE_SYSTEM, '', 'public'],
        ]

    def pre_process(self, content_dir, args, version=None):
        ret = []
        for scope_pair in self.get_scopes():
            scope = scope_pair[0]
            base_url_prefix = scope_pair[1]
            dest_dir = scope_pair[2]
            out_dir = os.path.join('./_output',
                                   'content_' + args.edition + "_" + scope)
            if version:
                out_dir = out_dir + "_" + version

            # clean out_dir first
            run_process('rm -rf %s' % out_dir)

            p = processor.DirProcess(content_dir, out_dir)
            p.\
                include_by_scope(scope).\
                include_by_edition(args.edition).\
                start()
            ret.append([out_dir, base_url_prefix, dest_dir])
        return ret

    def start(self, content_dir, args):
        if args.multi_versions:
            self.multi_versions_build(content_dir, args)
        else:
            self.singal_version_build(content_dir, args)

    def singal_version_build(self, content_dir, args):
        out_dirs = self.pre_process(content_dir, args)
        for out_dir in out_dirs:
            hugo = self.new_hugo(out_dir, args)
            hugo.execute()

    def new_hugo(self, out_dir_pair, args):
        out_dir = out_dir_pair[0]
        base_url_prefix = out_dir_pair[1]
        dest_dir = out_dir_pair[2]
        hugo = Hugo(out_dir)
        hugo.set_dest_dir(dest_dir)
        hugo.set_base_url_prefix(base_url_prefix)
        if args.host:
            hugo.set_host(args.host)
        if args.edition == processor.EDITION_EE:
            hugo.set_base_config('config-ee.toml')
        return hugo

    def update_branch(self, branch):
        run_process('git checkout -q %s' % branch)
        upstream_cmd = 'git rev-parse @{u}'
        local_cmd = 'git rev-parse @'
        upstream_out = run_process(upstream_cmd)
        local_out = run_process(local_cmd)
        if upstream_out != local_out:
            run_process('git merge -q upstream/%s' % branch)

    def check_and_update(self, version):
        branch = 'master'
        if version != 'master':
            branch = 'release/%s' % version
        self.update_branch(branch)

    def multi_versions_build(self, content_dir, args):
        versions = VERSION_ARRAY
        cur_branch = run_process('git rev-parse --abbrev-ref HEAD')
        print("args.out_fetch: %s" % args.out_fetch)
        if not args.out_fetch:
            run_process('git remote update')
        for version in versions:
            self.check_and_update(version)
            out_dirs = self.pre_process(content_dir, args, version=version)
            for out_dir in out_dirs:
                hugo = self.new_hugo(out_dir, args)
                hugo.set_current_version(version)
                hugo.set_versions(versions)
                hugo.execute()
        run_process('git checkout %s' % cur_branch)


class OnlineDriver(BaseDriver):

    def __init__(self):
        super(OnlineDriver, self).__init__(MODE_ONLINE)


__register_driver(MODE_ONLINE, OnlineDriver())


class OfflineDriver(BaseDriver):

    def __init__(self):
        super(OfflineDriver, self).__init__(MODE_OFFLINE)
        run_process('rm -rf ./public')

    def get_scopes(self):
        return [
            [processor.SCOPE_SYSTEM, '/docs/', 'public/docs'],
            [processor.SCOPE_DOMAIN, '/docs/domain', 'public/docs/domain'],
            [processor.SCOPE_PROJECT, '/docs/project', 'public/docs/project'],
        ]


__register_driver(MODE_OFFLINE, OfflineDriver())
