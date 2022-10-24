#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import textwrap

from converter import processor
from builder.consts import MODE_ONLINE, MODE_OFFLINE


def parse_args():
    parser = argparse.ArgumentParser(
        description="Use processor and hugo build document website.",
        formatter_class=argparse.RawTextHelpFormatter)

    bool_action = 'store_true'
    if hasattr(argparse, 'BooleanOptionalAction'):
        bool_action = argparse.BooleanOptionalAction
    parser.add_argument('--mode',
                        choices=[MODE_ONLINE, MODE_OFFLINE],
                        default=MODE_ONLINE,
                        help='''\
                            Build mode
                                online: Public website
                                offline: Docs inside ee edition
                            ''')
    parser.add_argument('--host', help="Hugo base url", default="")
    parser.add_argument('--edition', help="Build edition",
                            choices=[processor.EDITION_CE, processor.EDITION_EE],
                            default=processor.EDITION_CE)
    parser.add_argument('--multi-versions', help="Enable multi versions",
                        action=bool_action)
    parser.add_argument('--out-fetch', help="Not fetch upstream",
                        action=bool_action)

    args = parser.parse_args()

    return args


def start_build(args):
    mode = args.mode
    drv = get_build_driver(mode)
    drv.start('./content', args)


def get_build_driver(mode):
    from builder.drivers import get_driver
    return get_driver(mode)


if __name__ == '__main__':
    args = parse_args()
    start_build(args)
