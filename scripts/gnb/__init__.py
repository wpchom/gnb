#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from . import utils, build, clean, package, compress

sys.dont_write_bytecode = True


def _parser():
    parser = argparse.ArgumentParser(description="GNB buildtools")
    subparsers = parser.add_subparsers(title="module", dest="module")

    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    parser.add_argument("-x", "--proxy", type=str, default=os.getenv("GNB_PROXY"))

    subparsers.add_parser("update", aliases=["u"], help="update gnb")

    build.parser(subparsers)
    clean.parser(subparsers)
    package.parser(subparsers)

    parser.set_defaults(module="build")

    return parser


def _module(args):
    if (args.module == "update") or (args.module == "u"):
        utils.update_self()
    if (args.module == "build") or (args.module == "b"):
        build.module(args)
    elif (args.module == "clean") or (args.module == "c"):
        clean.module(args)
    elif (args.module == "package") or (args.module == "p"):
        package.module(args)
    else:
        utils.error(f"unknown module `{args.module}`")


def main():
    import pathlib

    args = _parser().parse_args()

    args.repo_dir = utils.GNB_REPO_DIR

    # TODO: read from config file
    args.pkgs_dir = os.path.join(args.repo_dir, "packages")

    args.cache_dir = os.path.join(pathlib.Path.home(), ".gnb", "cache")
    # args.cache_dir = os.path.join(args.repo_dir, "cache")

    if args.proxy != None:
        os.environ["GNB_PROXY"] = args.proxy

    if args.verbose:
        utils.debug(args)

    _module(args)

    if os.getenv("GNB_PROXY"):
        os.environ["GNB_PROXY"] = ""


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        utils.error("KeyboardInterrupt")
