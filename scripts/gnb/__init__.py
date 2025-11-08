#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import argparse
import subprocess

sys.dont_write_bytecode = True

GNB_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
GNB_GIT = "https://github.com/wpchom/gnb.git"

GN_DOWNLOAD_URL = (
    "https://chrome-infra-packages.appspot.com/dl/gn/gn/{plat_sys}-{plat_mach}/+/latest"
)
NINJA_DOWNLOAD_URL = (
    "https://github.com/ninja-build/ninja/releases/latest/download/ninja-{plat_sys}.zip"
)


def debug(*args):
    message = " ".join(str(arg) for arg in args)
    sys.stdout.write(f"{message}\n")
    sys.stdout.flush()


def info(*args):
    message = " ".join(str(arg) for arg in args)
    sys.stdout.write(f"\033[32m>>> {message}\033[0m\n")
    sys.stdout.flush()


def error(ret, *args):
    message = " ".join(str(arg) for arg in args)
    sys.stderr.write(f"\033[31m>>> {message}\033[0m\n")
    sys.stderr.flush()
    exit(ret)


def check_gn(cache_dir, proxy):
    gn_bin = shutil.which("gn")

    if gn_bin != None:
        ret = subprocess.run(
            [gn_bin, "--version"], stdout=subprocess.DEVNULL, check=False
        )
        if ret.returncode == 0:
            return gn_bin

    import platform

    plat_sys = platform.uname().system.lower()
    plat_sys = "mac" if plat_sys == "darwin" else plat_sys
    plat_sys = "win" if plat_sys == "windows" else plat_sys

    plat_mach = platform.uname().machine.lower()
    plat_mach = "arm64" if plat_mach == "aarch64" else plat_mach

    gn_bin = os.path.join(cache_dir, "bin", f"gn-{plat_sys}-{plat_mach}/gn")
    if not os.path.exists(gn_bin):
        import download, compress

        gn_download_path = os.path.dirname(gn_bin) + ".zip"
        if not os.path.exists(gn_download_path):
            download.download_pkg(GN_DOWNLOAD_URL, gn_download_path, proxy)
        compress.decompress(gn_download_path, os.path.dirname(gn_bin))

        os.chmod(gn_bin, 0o755)

    try:
        ret = subprocess.run([gn_bin, "--version"], stdout=subprocess.DEVNULL)
    except Exception:
        error(f"`{gn_bin}` error, please remove it to retry")

    return gn_bin


def check_ninja(cache_dir, proxy):
    ninja_bin = shutil.which("ninja")

    if ninja_bin != None:
        ret = subprocess.run(
            [ninja_bin, "--version"], stdout=subprocess.DEVNULL, check=False
        )
        if ret.returncode == 0:
            return ninja_bin

    import platform

    plat_sys = platform.uname().system.lower()
    plat_sys = "mac" if plat_sys == "darwin" else plat_sys

    ninja_bin = os.path.join(cache_dir, "bin", f"ninja-{plat_sys}/ninja")
    if not os.path.exists(ninja_bin):
        import download, compress

        ninja_download_path = os.path.dirname(ninja_bin) + ".zip"
        if not os.path.exists(ninja_download_path):
            download.download_pkg(NINJA_DOWNLOAD_URL, ninja_download_path, proxy)
        compress.decompress(ninja_download_path, os.path.dirname(ninja_bin))

        os.chmod(ninja_bin, 0o755)

    try:
        ret = subprocess.run([ninja_bin, "--version"], stdout=subprocess.DEVNULL)
    except Exception:
        error(f"`{ninja_bin}` error, please remove it to retry")

    return ninja_bin


def check_self(update=False):
    return
    if not ".git" in os.listdir(GNB_DIR):
        error(f"`{GNB_DIR}` is not a git repository")

    if not os.path.exists(GNB_DIR):
        try:
            subprocess.run(["git", "clone", GNB_GIT, GNB_DIR])
        except Exception as e:
            error(f"`git clone {GNB_GIT} {GNB_DIR}` failed", f"\n{str(e)}")
    elif update:
        try:
            subprocess.run(["git", "-C", GNB_DIR, "pull"])
        except Exception as e:
            error(f"`git -C {GNB_DIR} pull` failed", f"\n{str(e)}")


def parser():
    parser = argparse.ArgumentParser(description="GNB buildtools")
    subparsers = parser.add_subparsers(title="action", dest="action")

    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    parser.add_argument("-k", "--update", action="store_true", default=False)
    parser.add_argument(
        "-x",
        "--proxy",
        default=os.getenv("GNB_PROXY"),
        help="proxy server, default getenv GNB_PROXY",
    )

    from . import build, clean, package, compress

    build.parser(subparsers)
    clean.parser(subparsers)
    package.parser(subparsers)
    compress.parser(subparsers)

    parser.set_defaults(action="build")

    return parser


def action(args):
    args.gnb_dir = GNB_DIR
    args.cache_dir = os.path.join(GNB_DIR, "cache")

    if (args.action == "build") or (args.action == "b"):
        build.action(args)
    elif (args.action == "clean") or (args.action == "c"):
        clean.action(args)
    elif (args.action == "package") or (args.action == "p"):
        package.action(args)
    elif (args.action == "compress") or (args.action == "c"):
        compress.action(args)
    else:
        error(f"unknown action `{args.action}`")


def main():
    check_self(False)

    args = parser().parse_args()
    if args.verbose:
        debug(args)
    if args.proxy != None:
        os.environ["GNB_PROXY"] = args.proxy

    check_self(args.update)
    action(args)

    if os.getenv("GNB_PROXY"):
        os.environ["GNB_PROXY"] = ""


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        error(1, "KeyboardInterrupt")
