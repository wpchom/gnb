#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.dont_write_bytecode = True

import argparse
from . import utils, package, build, clean, download, compress


def _parser():
    parser = argparse.ArgumentParser(description="GNB buildtools")

    parser.add_argument(
        "-p", "--pkgs_dir", type=str, default=None, help="packages repos dir"
    )

    subparsers = parser.add_subparsers(title="action", dest="action")

    subparsers.add_parser("update", aliases=["u"], help="update gnb")
    package.parser(subparsers)
    build.parser(subparsers)
    clean.parser(subparsers)
    download.parser(subparsers)
    compress.parser(subparsers)

    parser.set_defaults(action="build")

    return parser.parse_args()


def _action(args):
    if (args.action == "update") or (args.action == "u"):
        utils.update(args)
    elif (args.action == "build") or (args.action == "b"):
        build.action(args)
    elif (args.action == "clean") or (args.action == "c"):
        clean.action(args)
    elif (args.action == "package") or (args.action == "p"):
        package.action(args)
    elif (args.action == "download") or (args.action == "d"):
        download.action(args)
    elif (args.action == "compress") or (args.action == "z"):
        compress.action(args)
    else:
        utils.error(f'Unknown action "{args.action}"')


def main():
    args = _parser()

    args.repo_dir = utils.GNB_REPO_DIR

    if args.pkgs_dir == None:
        if os.environ.get("GNB_PKGS_DIR") != None:
            args.pkgs_dir = os.environ.get("GNB_PKGS_DIR")
        else:
            args.pkgs_dir = os.path.join(args.repo_dir, "packages")
    if not os.path.exists(args.pkgs_dir):
        utils.error("Package source directory does not exist: " + args.pkgs_dir)

    _action(args)


if __name__ == "__main__":
    main()
