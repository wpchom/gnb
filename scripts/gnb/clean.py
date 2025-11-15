#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from . import utils

sys.dont_write_bytecode = True


def _parser_arguments(parser):
    parser.add_argument("outdir", help="output dir to clean")

    parser.add_argument("-v", "--verbose", action="store_true", default=False)


def parser(subparsers):
    parser = subparsers.add_parser("clean", aliases=["c"], help="clean build")
    _parser_arguments(parser)


def action(args):
    if (not os.path.exists(args.outdir)) or (
        not "build.ninja" in os.listdir(args.outdir)
    ):
        utils.info(f"`{args.outdir}` is not a build out dir")

    ninja_bin = utils.check_ninja(args.pkgs_dir, args.proxy)

    utils.info(f"Cleaning output directory `{args.outdir}`")

    ninja_cmd = [ninja_bin, "-C", args.outdir, "-t", "clean"]

    if args.verbose:
        utils.debug(" ".join(ninja_cmd))

    subprocess.run(ninja_cmd, check=True)
