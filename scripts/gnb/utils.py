#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess

from . import package

sys.dont_write_bytecode = True


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"

GNB_REPO_GIT = "https://github.com/wpchom/gnb.git"
GNB_REPO_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)


def debug(*args):
    message = " ".join(str(arg) for arg in args)
    sys.stdout.write(f"{message}\n")
    sys.stdout.flush()


def info(*args):
    message = " ".join(str(arg) for arg in args)
    sys.stdout.write(f"\033[32m>>> {message}\033[0m\n")
    sys.stdout.flush()


def error(*args):
    message = " ".join(str(arg) for arg in args)
    sys.stderr.write(f"\033[31m>>> {message}\033[0m\n")
    sys.stderr.flush()
    exit(1)


def check_gn(pkgs_dir, proxy):
    gn_bin = shutil.which("gn")

    if gn_bin == None:
        _, gn_bin = package.package_download("gn", "latest", pkgs_dir, proxy)

    return gn_bin


def check_ninja(pkgs_dir, proxy):
    ninja_bin = shutil.which("ninja")

    if ninja_bin == None:
        _, ninja_bin = package.package_download("ninja", "latest", pkgs_dir, proxy)

    return ninja_bin


def update_self():
    if not ".git" in os.listdir(GNB_REPO_DIR):
        error(f"`{GNB_REPO_DIR}` is not a git repository")

    git_bin = shutil.which("git")
    if git_bin == None:
        error("git is not installed")
    else:
        try:
            subprocess.run(
                [git_bin, "-C", GNB_REPO_DIR, "pull"], cwd=GNB_REPO_DIR, check=True
            )
        except Exception as e:
            error(f"`git -C {GNB_REPO_DIR} pull` failed", f"\n{str(e)}")
