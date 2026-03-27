#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.dont_write_bytecode = True

import shutil
import subprocess
from . import utils

_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"


def _parser_arguments(parser):
    parser.add_argument("url", type=str, help="url for download, or .git")

    parser.add_argument(
        "-x", "--proxy", type=str, default=os.getenv("GNB_PROXY"), help="download proxy"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="print verbose"
    )

    parser.add_argument(
        "-o", "--output", type=str, default=os.getcwd(), help="packages source dir"
    )
    parser.add_argument(
        "-t", "--timeout", type=int, default=1800, help="timeout for download"
    )
    parser.add_argument(
        "-u", "--user_agent", type=str, default=_USER_AGENT, help="user agent for http"
    )
    parser.add_argument(
        "-b", "--branch", type=str, default=None, help="branch of git repo"
    )


def parser(subparsers):
    parser = subparsers.add_parser("download", aliases=["d"], help="download package")
    _parser_arguments(parser)


def download_get_name(url, proxy=None, user_agent=None, timeout=None):
    import re
    from urllib.parse import urlparse

    curl_bin = shutil.which("curl")
    if not curl_bin:
        utils.error("`curl` not found")

    curl_command = [curl_bin, "-I", "-L", "-s"]
    curl_command += ["-w", "%{url_effective}"]
    curl_command += ["-o", "-"]

    if proxy:
        curl_command += ["--proxy", proxy]

    if user_agent:
        curl_command += ["-A", user_agent]

    if timeout:
        curl_command += ["--max-time", str(timeout)]

    try:
        ret = subprocess.check_output(curl_command + [url], text=True)
    except:
        utils.error(f"curl get header `{url}` failed")

    for line in ret.split("\n"):
        line = line.strip().lower()
        if line.startswith("content-disposition:"):
            match = re.search(r'filename="?([^";]+)', line)
            if match:
                return match.group(1).strip()

    final_url = ret.split("\n")[-1]
    if final_url.startswith("http"):
        return os.path.basename(urlparse(final_url).path)

    return None


def download_by_url(url, outdir=os.getcwd(), proxy=None, user_agent=None, timeout=None):
    filename = download_get_name(url, proxy, user_agent, timeout)
    if filename == None:
        utils.error(f"download `{url}` get filename failed")

    curl_bin = shutil.which("curl")
    if not curl_bin:
        utils.error("`curl` not found")

    curl_command = [curl_bin, "-#", "-L", "-f"]
    # curl_command += ["--write-out", "%{filename_effective}"]
    curl_command += ["-o", os.path.join(outdir, filename)]
    curl_command += ["-C", "-"]

    if proxy:
        curl_command += ["--proxy", proxy]

    if user_agent:
        curl_command += ["-A", user_agent]

    if timeout:
        curl_command += ["--max-time", str(timeout)]

    os.makedirs(outdir, exist_ok=True)

    ret = subprocess.run(
        curl_command + [url],
        stdout=sys.stdout,
        stderr=sys.stderr,
        text=True,
        check=False,
    )

    if ret.returncode != 0:
        utils.error(f"curl download `{url}` failed")

    return os.path.abspath(os.path.join(outdir, filename))


def download_by_git(url, outdir=os.getcwd(), branch=None, proxy=None):
    git_bin = shutil.which("git")
    if git_bin == None:
        utils.error("`git` not found")

    git_command = [git_bin, "clone", "--depth=1", "--recursive"]

    if branch:
        git_command += ["-b", branch]

    if proxy:
        git_command += ["-c", f"http.prox={proxy}", "-c", f"https.proxy={proxy}"]

    if os.path.exists(outdir):
        utils.error(f"{outdir} already exists")
    else:
        os.makedirs(os.path.dirname(outdir), exist_ok=True)

    ret = subprocess.run(
        git_command + [url, outdir],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    if ret.returncode:
        utils.error(f"git clone `{url}` failed")

    return os.path.abspath(outdir)


def action(args):
    if args.verbose:
        utils.debug(args)

    if args.url.endswith(".git"):
        outpath = download_by_git(args.url, args.output, args.branch, args.proxy)
    else:
        outpath = download_by_url(
            args.url, args.output, args.proxy, args.user_agent, args.timeout
        )

    utils.info(f"download `{args.url}` to `{outpath}`")
