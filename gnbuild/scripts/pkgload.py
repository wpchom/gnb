#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.dont_write_bytecode = True


def main():
    import argparse
    from gnb import package, utils

    parser = argparse.ArgumentParser(description="get gnb package path")
    parser.add_argument("package", metavar="PACKAGE", type=str, help="package name")
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

    pkglist = args.package.split(":")
    if len(pkglist) > 2:
        utils.error("Invalid package name")
    elif len(pkglist) == 2:
        pkgname = pkglist[0]
        pkgvers = pkglist[1]
    else:
        pkgname = pkglist[0]
        pkgvers = "latest"

    if args.pkgs_dir == None:
        if os.environ.get("MDS_PKGS_DIR") != None:
            args.pkgs_dir = os.environ.get("MDS_PKGS_DIR")
        else:
            mds_repo_dir = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            )
            args.pkgs_dir = os.path.join(mds_repo_dir, "packages")

    if not os.path.exists(args.pkgs_dir):
        utils.error(f"Package source directory does not exist: {args.pkgs_dir}")

    if not args.groupath:
        pkgvers, pkgpath = package.pkgload(
            args.pkgs_dir, pkgname, pkgvers, os.getenv("MDS_GNB_PROXY")
        )
        sys.stdout.write(f"{pkgvers}:{pkgpath}")
    else:
        pkgpath = package.pkgpath(args.pkgs_dir, pkgname)
        sys.stdout.write(f"{pkgpath}")


if __name__ == "__main__":
    main()
