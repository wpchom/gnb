#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess
from . import utils, clean

sys.dont_write_bytecode = True


def _parser_arguments(parser):
    parser.add_argument("target", nargs="?", default="default", help="target to build")
    parser.add_argument(
        "-b", "--builddir", default=None, help="build root directory for gn"
    )
    parser.add_argument("-d", "--dotfile", default=None, help="build dotfile for gn")
    parser.add_argument(
        "-o", "--outdir", default=None, help="build output directory for gn"
    )

    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    parser.add_argument(
        "-r",
        "--rebuild",
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


def module(args):
    if ("builddir" in args) and (args.builddir != None):
        args.builddir = os.path.abspath(args.builddir)
    else:
        args.builddir = os.path.abspath(os.getcwd())

    if ("dotfile" in args) and (args.dotfile != None):
        if os.path.exists(os.path.join(os.getcwd(), args.dotfile)):
            args.dotfile = os.path.abspath(args.dotfile)
        elif os.path.exists(os.path.join(args.builddir, args.dotfile)):
            args.dotfile = os.path.join(args.builddir, args.dotfile)
        else:
            dotfile = os.path.join(args.repo_dir, "dotfiles", args.dotfile)
            if not dotfile.endswith(".gn"):
                dotfile += ".gn"
            if os.path.exists(dotfile):
                args.dotfile = dotfile
            else:
                utils.error(f"`{args.dotfile}` not exists")
    else:
        args.dotfile = os.path.join(args.repo_dir, "dotfiles", "debug.gn")

    if ("outdir" in args) and (args.outdir != None):
        args.outdir = os.path.abspath(args.outdir)
    else:
        args.outdir = os.path.join(os.getcwd(), "outdir")

    if not "args" in args:
        args.args = []

    if ("rebuild" in args) and args.rebuild:
        clean.module(args)

    build_action(
        args.builddir,
        args.dotfile,
        args.outdir,
        args.args,
        args.repo_dir,
        args.pkgs_dir,
        args.cache_dir,
        args.proxy,
        args.verbose,
    )


def build_action(
    builddir, dotfile, outdir, buildargs, repo_dir, pkgs_dir, cache_dir, proxy, verbose
):
    stime = time.perf_counter()
    utils.info(f"Building action start `{builddir}` with `{dotfile}`")

    # gn gen
    gn_bin = utils.check_gn(pkgs_dir, cache_dir, proxy)
    gn_command = [gn_bin, "gen", outdir, "--export-compile-commands"]
    gn_command += ["--root=%s" % builddir, "--dotfile=%s" % dotfile]

    buildargs = [f'gnb_pkgs_dir="{pkgs_dir}"'] + buildargs if buildargs else []
    gn_command += ["--args=%s" % " ".join(buildargs)]

    if verbose:
        utils.debug(" ".join(gn_command))

    # git ignore
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, ".gitignore"), "w+") as f:
        f.write("*\n")

    ret = subprocess.run(
        gn_command, cwd=builddir, check=False, env={"GNB_REPO_DIR": repo_dir}
    )
    if ret.returncode != 0:
        utils.error(" ".join(gn_command))

    # ninja build
    ninja_bin = utils.check_ninja(pkgs_dir, cache_dir, proxy)
    ninja_command = [ninja_bin, "-C", outdir]

    if verbose:
        ninja_command += ["-v"]
        utils.debug(" ".join(ninja_command))

    ret = subprocess.run(ninja_command, cwd=outdir, check=False)

    # complete
    etime = time.perf_counter()
    if ret.returncode == 0:
        utils.info(f"Building action finished cost time: {etime - stime:.3f}s")
    else:
        utils.error(f"Building action error cost time: {etime - stime:.3f}s")
