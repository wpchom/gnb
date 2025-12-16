#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.dont_write_bytecode = True

import argparse
from . import utils, build, clean, package, compress


def _parser():
    parser = argparse.ArgumentParser(description="GNB buildtools")
    subparsers = parser.add_subparsers(title="action", dest="action")

    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    parser.add_argument("-x", "--proxy", type=str, default=os.getenv("GNB_PROXY"))

    subparsers.add_parser("update", aliases=["u"], help="update gnb")

    build.parser(subparsers)
    clean.parser(subparsers)
    package.parser(subparsers)
    compress.parser(subparsers)

    parser.set_defaults(action="build")

    return parser


def _action(args):
    if (args.action == "update") or (args.action == "u"):
        utils.update_self()
    elif (args.action == "build") or (args.action == "b"):
        build.action(args)
    elif (args.action == "clean") or (args.action == "c"):
        clean.action(args)
    elif (args.action == "package") or (args.action == "p"):
        package.action(args)
    elif (args.action == "compress") or (args.action == "z"):
        compress.action(args)
    else:
        utils.error(f'Unknown action "{args.action}"')


def main():
    args = _parser().parse_args()

    args.repo_dir = utils.GNB_REPO_DIR

    # TODO: read from config file
    args.pkgs_dir = os.path.join(args.repo_dir, "packages")

    if args.proxy != None:
        os.environ["GNB_PROXY"] = args.proxy

    if args.verbose:
        utils.debug(args)

    _action(args)

    if os.getenv("GNB_PROXY"):
        os.environ["GNB_PROXY"] = ""


if __name__ == "__main__":
    main()
