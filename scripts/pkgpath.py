#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse

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

    args = parser.parse_args()

    sys.stdout.write(os.path.join(args.pkgsrc, args.pkgname[0], args.pkgname))


if __name__ == "__main__":
    main()
