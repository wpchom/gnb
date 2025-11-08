#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from . import debug, info, error

sys.dont_write_bytecode = True


def parser(subparsers):
    parser = subparsers.add_parser("package", aliases=["p"], help="package manager")

    parser.add_argument("outdir", help="output dir to clean")

    parser.add_argument("-v", "--verbose", action="store_true", default=False)


def action(args):
    from . import check_ninja

    if (not os.path.exists(args.outdir)) or (
        not "build.ninja" in os.listdir(args.outdir)
    ):
        error(0, f"`{args.outdir}` is not a build out dir")

    ninja_bin = check_ninja(args.cache_dir, args.proxy)

    info(f"Cleaning output directory `{args.outdir}`")

    ninja_cmd = [ninja_bin, "-C", args.outdir, "-t", "clean"]

    if args.verbose:
        debug(" ".join(ninja_cmd))

    subprocess.run(ninja_cmd, check=True)
