#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.dont_write_bytecode = True

from . import utils


def _parser_arguments(parser):
    parser.add_argument("-p", "--profile", default=None, help="build profile for gn")
    parser.add_argument(
        "-o", "--output", default=None, help="build output directory for gn"
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="print verbose"
    )


def parser(subparsers):
    parser = subparsers.add_parser("clean", aliases=["c"], help="clean build")
    _parser_arguments(parser)


def run_clean(output, pkgs_dir, verbose=False, proxy=None):
    import subprocess

    if (not os.path.exists(output)) or (not "build.ninja" in os.listdir(output)):
        utils.info(f"`{output}` is not a build out dir")
        return

    ninja_bin = utils.check_ninja(pkgs_dir, proxy)

    utils.info(f"Cleaning output directory `{output}`")

    ninja_command = [ninja_bin, "-C", output, "-t", "clean"]

    if verbose:
        ninja_command.append("-v")
        utils.debug(" ".join(ninja_command))

    ret = subprocess.run(
        ninja_command, cwd=output, stdout=sys.stdout, stderr=sys.stderr
    )

    if ret.returncode != 0:
        utils.info("Cleaning action error")


def action(args):
    from . import build

    if ("builddir" in args) and (args.builddir != None):
        args.builddir = os.path.abspath(args.builddir)
    else:
        args.builddir = os.path.abspath(os.getcwd())

    args.profile = build.get_profile(args.repo_dir, args.builddir, args.profile)

    if ("output" in args) and (args.output != None):
        args.output = os.path.abspath(args.output)
    else:
        args.output = os.path.join(
            os.getcwd(), "output", os.path.splitext(os.path.basename(args.profile))[0]
        )

    if args.verbose:
        utils.debug(args)

    run_clean(args.output, args.pkgs_dir, args.verbose)
