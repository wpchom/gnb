#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import importlib
import pathlib

sys.dont_write_bytecode = True


def main():
    gnb_repo_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    parser = argparse.ArgumentParser(description="get gnb package path")
    parser.add_argument("pkgname", metavar="PKGNAME", type=str, help="package name")
    parser.add_argument(
        "--pkgsrc",
        default=os.path.join(gnb_repo_dir, "packages"),
        help="packages sources",
    )
    parser.add_argument(
        "-d", "--download", action="store_true", default=False, help="download package"
    )

    args = parser.parse_args()

    if ":" in args.pkgname:
        _pkgname = args.pkgname.split(":")[0]
        args.version = args.pkgname[len(_pkgname) + 1 :]
        args.pkgname = _pkgname
    else:
        args.version = "latest"

    if args.download:
        from gnb import package

        _, pkgpath = package.package_download(
            args.pkgname, args.version, args.pkgsrc, os.getenv("GNB_PROXY")
        )
    else:
        pkgpath = os.path.join(args.pkgsrc, args.pkgname[0], args.pkgname)

    sys.stdout.write(pkgpath)


if __name__ == "__main__":
    main()
