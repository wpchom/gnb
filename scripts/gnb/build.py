#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.dont_write_bytecode = True

from . import utils, clean


def _parser_arguments(parser):
    parser.add_argument("target", nargs="?", default=None, help="target to build")
    parser.add_argument(
        "-b", "--builddir", default=None, help="build root directory for gn"
    )
    parser.add_argument("-p", "--profile", default=None, help="build profile for gn")
    parser.add_argument(
        "-o", "--outdir", default=None, help="build output directory for gn"
    )

    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        default=False,
        help="clean outdir before build",
    )
    parser.add_argument(
        "-x",
        "--proxy",
        default=os.getenv("GNB_PROXY"),
        help="proxy server, default getenv GNB_PROXY",
    )

    parser.add_argument("--args", action="append", default=[], help="gn gen with args")


def parser(subparsers):
    parser = subparsers.add_parser("build", aliases=["b"], help="build project")
    _parser_arguments(parser)


def get_profile(repo_dir, builddir, profile, default="debug.gn"):
    if profile != None:
        if os.path.exists(os.path.join(os.getcwd(), profile)):
            return os.path.join(os.getcwd(), profile)
        elif os.path.exists(os.path.join(builddir, profile)):
            return os.path.join(builddir, profile)
        else:
            profile = os.path.join(repo_dir, "gnbuild", "profiles", profile)
            if not profile.endswith(".gn"):
                profile += ".gn"
            if os.path.exists(profile):
                return profile
            else:
                utils.error(f"({profile}) not exists")
    else:
        default_profile = os.path.join(repo_dir, "gnbuild", "profiles", default)
        if os.path.exists(default_profile):
            return default_profile
        else:
            utils.error(f"Default profile `{default_profile}` not exists. ")


def action(args):
    if ("builddir" in args) and (args.builddir != None):
        args.builddir = os.path.abspath(args.builddir)
    else:
        args.builddir = os.path.abspath(os.getcwd())

    args.profile = get_profile(args.repo_dir, args.builddir, args.profile)

    if ("outdir" in args) and (args.outdir != None):
        args.outdir = os.path.abspath(args.outdir)
    else:
        args.outdir = os.path.join(os.getcwd(), "outdir")

    if not "args" in args:
        args.args = []

    if ("clean" in args) and args.clean:
        clean.action(args)

    build_action(
        args.builddir,
        args.profile,
        args.outdir,
        args.args,
        args.repo_dir,
        args.pkgs_dir,
        args.proxy,
        args.verbose,
        args.target if ("target" in args) and (args.target != "") else None,
    )


def build_action(
    builddir,
    profile,
    outdir,
    buildargs,
    repo_dir,
    pkgs_dir,
    proxy,
    verbose,
    target=None,
):
    import time, subprocess

    stime = time.perf_counter()
    utils.info(f"Building action start `{builddir}` with `{profile}`")

    buildout = os.path.join(outdir, os.path.splitext(os.path.basename(profile))[0])

    # gn gen
    gn_bin = utils.check_gn(pkgs_dir, proxy)
    gn_command = [gn_bin, "gen", buildout, "--export-compile-commands"]
    gn_command += ["--root=%s" % builddir, "--dotfile=%s" % profile]

    buildargs = [f'gnb_pkgs_dir="{pkgs_dir}"'] + (buildargs if buildargs else [])
    gn_command += ["--args=%s" % " ".join(buildargs)]

    if verbose:
        utils.debug(" ".join(gn_command))

    # git ignore
    os.makedirs(buildout, exist_ok=True)
    with open(os.path.join(buildout, ".gitignore"), "w+") as f:
        f.write("*\n")

    ret = subprocess.run(
        gn_command,
        cwd=builddir,
        check=False,
        env={**os.environ, "GNB_REPO_DIR": repo_dir},
    )
    if ret.returncode != 0:
        utils.error(" ".join(gn_command))

    # ninja build
    ninja_bin = utils.check_ninja(pkgs_dir, proxy)
    ninja_command = [ninja_bin, "-C", buildout]

    if (target != None) and (target != ""):
        ninja_command += [target]

    if verbose:
        ninja_command += ["-v"]
        utils.debug(" ".join(ninja_command))

    ret = subprocess.run(ninja_command, cwd=buildout, check=False)

    # complete
    etime = time.perf_counter()
    if ret.returncode == 0:
        utils.info(f"Building action finished cost time: {etime - stime:.3f}s")
    else:
        utils.error(f"Building action error cost time: {etime - stime:.3f}s")
