#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.dont_write_bytecode = True

from . import utils


def _parser_arguments(parser):
    parser.add_argument("outdir", help="output dir to clean")


def parser(subparsers):
    parser = subparsers.add_parser("clean", aliases=["c"], help="clean build")
    _parser_arguments(parser)


def action(args):
    import subprocess

    if (not os.path.exists(args.outdir)) or (
        not "build.ninja" in os.listdir(args.outdir)
    ):
        utils.info(f"`{args.outdir}` is not a build out dir")
        return

    ninja_bin = utils.check_ninja(args.pkgs_dir, args.proxy)

    utils.info(f"Cleaning output directory `{args.outdir}`")

    ninja_cmd = [ninja_bin, "-C", args.outdir, "-t", "clean"]

    if args.verbose:
        utils.debug(" ".join(ninja_cmd))

    subprocess.run(ninja_cmd, check=True)
