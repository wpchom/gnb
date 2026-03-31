#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.dont_write_bytecode = True

from . import utils


def _parser_arguments(parser):
    parser.add_argument(
        "-x", "--proxy", default=os.getenv("MDS_GNB_PROXY"), help="download proxy"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="print verbose"
    )


def parser(subparsers):
    parser = subparsers.add_parser("update", aliases=["u"], help="update check")
    _parser_arguments(parser)


def action(args):
    import subprocess

    if args.verbose:
        utils.debug(args)

    if not ".git" in os.listdir(utils.MDS_REPO_DIR):
        utils.error(f"`{utils.MDS_REPO_DIR}` is not a git repository")

    git_bin = utils.check_git(utils.MDS_REPO_DIR, args.proxy)

    git_command = [git_bin, "-C", utils.MDS_REPO_DIR, "fetch"]

    if args.proxy:
        git_command += [
            "-c",
            f"http.prox={args.proxy}",
            "-c",
            f"https.proxy={args.proxy}",
        ]

    try:
        subprocess.run(
            git_command,
            cwd=utils.MDS_REPO_DIR,
            stdout=sys.stdout,
            stderr=sys.stderr,
            check=True,
        )
    except Exception as e:
        utils.error(f"`git -C {utils.MDS_REPO_DIR} pull` failed", f"\n{str(e)}")
