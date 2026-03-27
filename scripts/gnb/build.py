#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.dont_write_bytecode = True

import subprocess
from . import utils


def _parser_arguments(parser):
    parser.add_argument("target", nargs="?", default=None, help="target to build")

    parser.add_argument(
        "-x", "--proxy", default=os.getenv("GNB_PROXY"), help="download proxy"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="print verbose"
    )

    parser.add_argument(
        "-b", "--builddir", default=None, help="build root directory for gn"
    )
    parser.add_argument(
        "-p", "--profile", default=None, help="build profile of project for gn"
    )
    parser.add_argument(
        "-o", "--output", default=None, help="build output directory for gn"
    )
    parser.add_argument(
        "-c", "--clean", action="store_true", default=False, help="clean before build"
    )

    parser.add_argument("--args", action="append", default=[], help="gn gen with args")


def parser(subparsers):
    parser = subparsers.add_parser("build", aliases=["b"], help="build project")
    _parser_arguments(parser)


def get_profile(repo_dir, builddir, profile, default="debug.gn"):
    if profile != None:
        gnpfile = os.path.join(builddir, "profiles", profile)
        if not gnpfile.endswith(".gn"):
            gnpfile += ".gn"
        if os.path.exists(gnpfile):
            return gnpfile

        gnpfile = os.path.join(repo_dir, "gnbuild", "profiles", profile)
        if not gnpfile.endswith(".gn"):
            gnpfile += ".gn"
        if os.path.exists(gnpfile):
            return gnpfile

        utils.error(f"({profile}) not exists")
    else:
        default_profile = os.path.join(repo_dir, "gnbuild", "profiles", default)
        if os.path.exists(default_profile):
            return default_profile
        else:
            utils.error(f"Default profile `{default_profile}` not exists. ")


def action(args):
    from . import clean

    if ("builddir" in args) and (args.builddir != None):
        args.builddir = os.path.abspath(args.builddir)
    else:
        args.builddir = os.path.abspath(os.getcwd())

    args.profile = get_profile(args.repo_dir, args.builddir, args.profile)

    if ("output" in args) and (args.output != None):
        args.output = os.path.abspath(args.output)
    else:
        args.output = os.path.join(
            os.getcwd(), "output", os.path.splitext(os.path.basename(args.profile))[0]
        )

    if not "args" in args:
        args.args = []

    if args.verbose:
        utils.debug(args)

    if ("clean" in args) and args.clean:
        clean.run_clean(args.output, args.pkgs_dir, args.verbose, args.proxy)

    run_build(
        args.builddir,
        args.profile,
        args.output,
        args.args,
        args.repo_dir,
        args.pkgs_dir,
        args.verbose,
        args.proxy,
        args.target,
    )


def run_build(
    builddir,
    profile,
    output,
    buildargs,
    repo_dir,
    pkgs_dir,
    verbose=False,
    proxy=None,
    target=None,
):
    import time

    stime = time.perf_counter()
    utils.info(f"Building action start `{builddir}` with `{profile}`")

    # gn gen
    gn_bin = utils.check_gn(pkgs_dir, proxy)
    gn_command = [gn_bin, "gen", output, "--export-compile-commands"]
    gn_command += ["--root=%s" % builddir, "--dotfile=%s" % profile]

    buildargs = [f'gnb_pkgs_dir="{pkgs_dir}"'] + (buildargs if buildargs else [])
    gn_command += ["--args=%s" % " ".join(buildargs)]

    if verbose:
        gn_command += ["--time"]
        utils.debug(" ".join(gn_command))

    # git ignore
    os.makedirs(output, exist_ok=True)
    with open(os.path.join(output, ".gitignore"), "w+") as f:
        f.write("*\n")

    ret = subprocess.run(
        gn_command,
        cwd=builddir,
        stdout=sys.stdout,
        stderr=sys.stderr,
        env={**os.environ, "GNB_REPO_DIR": repo_dir},
    )
    if ret.returncode != 0:
        utils.error(" ".join(gn_command))

    # ninja build
    ninja_bin = utils.check_ninja(pkgs_dir, proxy)
    ninja_command = [ninja_bin, "-C", output]

    if (target != None) and (target != ""):
        ninja_command += [target]

    if verbose:
        ninja_command += ["-v"]
        utils.debug(" ".join(ninja_command))

    ret = subprocess.run(
        ninja_command, cwd=output, stdout=sys.stdout, stderr=sys.stderr
    )

    # complete
    etime = time.perf_counter()
    if ret.returncode == 0:
        utils.info(f"Building action finished cost time: {etime - stime:.3f}s")
    else:
        utils.error(f"Building action error cost time: {etime - stime:.3f}s")
