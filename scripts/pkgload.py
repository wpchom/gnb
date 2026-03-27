#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.dont_write_bytecode = True


def main():
    import argparse
    from gnb import package, utils

    gnb_repo_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    parser = argparse.ArgumentParser(description="get gnb package path")
    parser.add_argument("pkgname", metavar="PKGNAME", type=str, help="package name")
    parser.add_argument(
        "-v", "--version", type=str, default=None, help="package version"
    )
    parser.add_argument(
        "-p", "--pkgs_dir", type=str, default=None, help="packages repos dir"
    )
    parser.add_argument(
        "-g",
        "--groupath",
        action="store_true",
        default=False,
        help="path for package group",
    )

    args = parser.parse_args()

    if args.pkgs_dir == None:
        if os.environ.get("GNB_PKGS_DIR") != None:
            args.pkgs_dir = os.environ.get("GNB_PKGS_DIR")
        else:
            args.pkgs_dir = os.path.join(gnb_repo_dir, "packages")

    if not os.path.exists(args.pkgs_dir):
        utils.error(f"Package source directory does not exist: {args.pkgs_dir}")

    outpath = None

    if not args.groupath:
        _, outpath = package.pkgload(
            args.pkgs_dir, args.pkgname, args.version, os.getenv("GNB_PROXY")
        )
    else:
        outpath = package.pkgpath(args.pkgs_dir, args.pkgname)

    if outpath == None:
        utils.error(f"Package `{args.pkgname}:{args.version}` not found")

    sys.stdout.write(outpath)


if __name__ == "__main__":
    main()
