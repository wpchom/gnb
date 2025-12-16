#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.dont_write_bytecode = True

from . import utils, build


def _parser_arguments(parser):
    parser.add_argument("-p", "--profile", default=None, help="build profile for gn")
    parser.add_argument(
        "-o", "--outdir", default=None, help="build output directory for gn"
    )


def parser(subparsers):
    parser = subparsers.add_parser("clean", aliases=["c"], help="clean build")
    _parser_arguments(parser)


def clean_action(outdir, pkgs_dir, proxy, verbose):
    import subprocess

    if (not os.path.exists(outdir)) or (not "build.ninja" in os.listdir(outdir)):
        utils.info(f"`{outdir}` is not a build out dir")
        return

    ninja_bin = utils.check_ninja(pkgs_dir, proxy)

    utils.info(f"Cleaning output directory `{outdir}`")

    ninja_cmd = [ninja_bin, "-C", outdir, "-t", "clean"]

    if verbose:
        utils.debug(" ".join(ninja_cmd))

    subprocess.run(ninja_cmd, check=True)


def action(args):
    if ("builddir" in args) and (args.builddir != None):
        args.builddir = os.path.abspath(args.builddir)
    else:
        args.builddir = os.path.abspath(os.getcwd())

    args.profile = build.get_profile(args.repo_dir, args.builddir, args.profile)

    if ("outdir" in args) and (args.outdir != None):
        args.outdir = os.path.abspath(args.outdir)
    else:
        args.outdir = os.path.join(
            os.getcwd(), "outdir", os.path.splitext(os.path.basename(args.profile))[0]
        )

    clean_action(args.outdir, args.pkgs_dir, args.proxy, args.verbose)
