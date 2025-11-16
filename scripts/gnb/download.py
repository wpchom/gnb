#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess
from . import utils

sys.dont_write_bytecode = True


def _download_by_curl(url, dir, proxy=None, cont=False, timeout=30):
    curl_bin = shutil.which("curl")
    if curl_bin == None:
        utils.error("`curl` not found")

    curl_command = [
        curl_bin,
        "-OsL",
        "--max-time",
        str(timeout),
        "--write-out",
        "%{filename_effective}",
        "--user-agent",
        utils.USER_AGENT,
    ]

    if proxy != None:
        curl_command += ["--proxy", proxy]

    if cont:
        curl_command += ["-C", "-"]
    else:
        curl_command += ["-J"]

    ret = subprocess.run(
        curl_command + ["--parallel", url], cwd=dir, check=False, capture_output=True
    )
    if ret.returncode == 2:
        ret = subprocess.run(
            curl_command + [url], cwd=dir, check=False, capture_output=True
        )

    return ret


def download_file_exists(download_path):
    download_dir = os.path.dirname(download_path)
    download_name = os.path.basename(download_path)

    if os.path.exists(download_dir):
        for f in os.listdir(download_dir):
            if f.startswith(download_name + "."):
                return download_dir, f

    return download_dir, None


def download_from_url(url, download_path, proxy, remove=False, timeout=30):
    download_dir, download_name = download_file_exists(download_path)

    if download_name != None:
        if remove:
            shutil.rmtree(os.path.join(download_dir, download_name))
        else:
            return os.path.join(download_dir, download_name)

    os.makedirs(download_dir, exist_ok=True)
    download_tmp = os.path.join(download_dir, f"_{download_name}.tmp")

    if remove and os.path.exists(download_tmp):
        shutil.rmtree(download_tmp)

    if not os.path.exists(download_tmp):
        os.makedirs(download_tmp, exist_ok=True)
        ret = _download_by_curl(url, download_tmp, proxy, False, timeout)
    else:
        ret = _download_by_curl(url, download_tmp, proxy, True, timeout)

    try:
        download_file = ret.stdout.decode().strip()
        if download_file.split(".")[-2] in ["tar"]:
            download_name = f"{download_name}.{download_file.split('.')[-2]}.{download_file.split('.')[-1]}"
        else:
            download_name = f"{download_name}.{download_file.split('.')[-1]}"

        shutil.move(
            os.path.join(download_tmp, download_file),
            os.path.join(download_dir, download_name),
        )

        if os.path.exists(download_tmp):
            shutil.rmtree(download_tmp)

        return os.path.join(download_dir, download_name)

    except:
        shutil.rmtree(download_tmp)
        utils.error(f"Download `{url}` error: {ret.stderr.decode().strip()}")


def download_from_git(url, branch, path, proxy):
    git_bin = shutil.which("git")
    if git_bin == None:
        utils.error("`git` not found")

    if (not os.path.exists(path)) or (not ".git" in os.listdir(path)):
        try:
            os.makedirs(path, exist_ok=True)
            git_command = [git_bin, "clone", url, path, "--depth=1", "--recursive"]
            if branch != None:
                git_command += ["-b", branch]
            if proxy != None:
                git_command += [
                    "-c",
                    f"http.proxy={proxy}",
                    "-c",
                    f"https.proxy={proxy}",
                ]

            ret = subprocess.run(git_command, check=False)
            if ret.returncode != 0:
                utils.error(f"git clone `{url}` failed")

        except KeyboardInterrupt:
            try:
                shutil.rmtree(path)
            except:
                pass
            raise (KeyboardInterrupt)

    else:
        try:
            git_command = [git_bin, "status"]
            ret = subprocess.run(git_command, cwd=path, capture_output=True)

            if b"Changes not staged for commit" in ret.stdout.strip() or (
                b"Changes to be committed" in ret.stdout.strip()
            ):
                utils.error(f"git repository `{path}` has uncommitted changes")

            git_command = [git_bin, "fetch", "--all"]
            ret = subprocess.run(git_command, cwd=path)
            if ret.returncode != 0:
                utils.error(f"git fetch `{path}` failed")

            git_command = [git_bin, "checkout", branch]
            ret = subprocess.run(git_command, cwd=path)
            if ret.returncode != 0:
                utils.error(f"git checkout ({branch}) failed")

        except Exception:
            utils.error(
                f"git `{url}` branch ({branch}) fetch failed, remove it to retry"
            )
