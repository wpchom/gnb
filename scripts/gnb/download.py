#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.dont_write_bytecode = True

import shutil, subprocess
from . import utils, compress


def _download_by_curl(url, dir, proxy=None, remove=False, timeout=1800):
    curl_bin = shutil.which("curl")
    if curl_bin == None:
        utils.error("`curl` not found")

    curl_command = [curl_bin, "-sL", "-C", "-"]
    curl_command += ["--max-time", str(timeout)]
    curl_command += ["--write-out", "%{filename_effective}"]
    curl_command += ["--user-agent", utils.USER_AGENT]

    if proxy != None:
        curl_command += ["--proxy", proxy]

    ret = subprocess.run(
        curl_command + ["--parallel", "-O", url],
        cwd=dir,
        check=True,
        capture_output=True,
    )

    if ret.returncode == 2:
        ret = subprocess.run(
            curl_command + ["-O", url],
            cwd=dir,
            check=True,
            capture_output=True,
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


def _download_file_is_archive(filename):
    name_split = filename.split(".")
    if (len(name_split) > 1) and (name_split[-2] in ["tar"]):
        return filename[: -(len(name_split[-2]) + len(name_split[-1]) + 2)]
    elif name_split[-1] in ["tgz", "tbz2", "txz", "rar", "zip", "7z"]:
        return filename[: -(len(name_split[-1]) + 1)]
    else:
        return None


def download_from_url(url, download_path, proxy, remove=False, timeout=30):
    download_dir, download_name = download_file_exists(download_path)

    if download_name != None:
        if remove:
            os.remove(os.path.join(download_dir, download_name))
        elif _download_file_is_archive(download_name) != None:
            return os.path.join(download_dir, download_name)

    os.makedirs(download_dir, exist_ok=True)
    download_tmp = download_path + ".tmp"

    if remove and os.path.exists(download_tmp):
        shutil.rmtree(download_tmp)

    if not os.path.exists(download_tmp):
        os.makedirs(download_tmp, exist_ok=True)

    ret = _download_by_curl(url, download_tmp, proxy, timeout)
    if ret.returncode != 0:
        utils.error(f"Download `{url}` error: {ret.stderr.decode().strip()}")

    try:
        download_file = ret.stdout.decode().strip()
        download_name = os.path.basename(download_path)
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


def _download_decompress_archive(input_dir, decomp_dir, depth=1):
    if depth <= 0:
        return

    for fd in os.listdir(input_dir):
        if os.path.isdir(os.path.join(input_dir, fd)):
            _download_decompress_archive(
                os.path.join(input_dir, fd), os.path.join(decomp_dir, fd), depth - 1
            )
        else:
            filename = _download_file_is_archive(fd)
            if filename != None:
                compress.decompress(
                    os.path.join(input_dir, fd),
                    os.path.join(decomp_dir, filename),
                    True,
                )


def download_to_decompress(download_pkg, resource_path):
    compress.decompress(download_pkg, resource_path, True)

    _download_decompress_archive(resource_path, resource_path, 3)


def download_from_git(url, branch, path, proxy=None):
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
                if os.path.exists(path):
                    shutil.rmtree(path)
            except:
                pass
            raise (KeyboardInterrupt)

    else:
        try:
            git_command = [git_bin, "status", "--porcelain"]
            ret = subprocess.run(git_command, cwd=path, capture_output=True, text=True)

            if ret.stdout.strip():
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
