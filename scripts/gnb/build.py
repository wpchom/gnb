#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from . import debug, info, error

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


def action(args):
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
            dotfile = os.path.join(args.gnb_dir, "dotfiles", args.dotfile)
            if not dotfile.endswith(".gn"):
                dotfile += ".gn"
            if os.path.exists(dotfile):
                args.dotfile = dotfile
            else:
                error(1, f"`{args.dotfile}` not exists")
    else:
        args.dotfile = os.path.join(args.gnb_dir, "dotfiles", "debug.gn")

    if ("outdir" in args) and (args.outdir != None):
        args.outdir = os.path.abspath(args.outdir)
    else:
        args.outdir = os.path.join(os.getcwd(), "outdir")

    if not "args" in args:
        args.args = []

    if ("rebuild" in args) and args.rebuild:
        from . import clean

        clean.action(args)

    _build(args)


def _build(args):
    import time, subprocess
    from . import check_gn, check_ninja

    stime = time.perf_counter()
    info(f"Building action start `{args.builddir}` with `{args.dotfile}`")

    # gn gen
    gn_bin = check_gn(args.cache_dir, args.proxy)
    gn_command = [gn_bin, "gen", args.outdir, "--export-compile-commands"]
    gn_command += ["--root=%s" % args.builddir, "--dotfile=%s" % args.dotfile]

    if len(args.args) > 0:
        gn_command += ["--args=%s" % " ".join(args.args)]

    if args.verbose:
        debug(" ".join(gn_command))

    # git ignore
    os.makedirs(args.outdir, exist_ok=True)
    with open(os.path.join(args.outdir, ".gitignore"), "w+") as f:
        f.write("*\n")

    ret = subprocess.run(
        gn_command, cwd=args.builddir, check=False, env={"GNB_DIR": args.gnb_dir}
    )
    if ret.returncode != 0:
        error(ret.returncode, " ".join(gn_command))

    # ninja build
    ninja_bin = check_ninja(args.cache_dir, args.proxy)
    ninja_command = [ninja_bin, "-C", args.outdir]

    if args.verbose:
        ninja_command += ["-v"]
        debug(" ".join(ninja_command))

    ret = subprocess.run(ninja_command, cwd=args.outdir, check=False)

    # complete
    etime = time.perf_counter()
    if ret.returncode == 0:
        info(f"Building action finished cost time: {etime - stime:.3f}s")
    else:
        error(
            ret.returncode,
            f"Building action error cost time: {etime - stime:.3f}s",
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    _parser_arguments(parser)

    args = parser.parse_args()
    args.gnb_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    args.cache_dir = os.path.join(args.gnb_dir, "cache")

    try:
        action(args)
    except KeyboardInterrupt:
        error(1, "KeyboardInterrupt")
