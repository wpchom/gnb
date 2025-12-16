#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.dont_write_bytecode = True

import shutil
from . import utils


def _parser_arguments(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--compress", action="store_true", help="compress")
    group.add_argument("-d", "--decompress", action="store_true", help="decompress")

    parser.add_argument(
        "-f", "--force", action="store_true", default=False, help="force"
    )
    parser.add_argument("inpath", help="input path")
    parser.add_argument("outpath", help="output path")


def parser(subparsers):
    parser = subparsers.add_parser(
        "compress", aliases=["e"], help="compress or decompress"
    )
    _parser_arguments(parser)


def compress(input_path, output_file, force):
    utils.error("Compress not implemented")


def decompress(input_file, output_path, force):
    if output_path == None:
        output_path = os.path.dirname(input_file)

    if os.path.exists(output_path):
        if force:
            shutil.rmtree(output_path)
        else:
            utils.error(f"Output directory already exists: `{output_path}`")

    if (input_file.split(".")[-2] in ["tar"]) or (
        input_file.split(".")[-1] in ["tgz", "tbz2", "txz"]
    ):
        import tarfile

        with tarfile.open(input_file) as tar:
            tar.extractall(output_path)
        return

    elif input_file.split(".")[-1] in ["zip"]:
        import zipfile

        with zipfile.ZipFile(input_file) as zip:
            zip.extractall(output_path)
        return
    elif input_file.split(".")[-1] in ["rar"]:
        try:
            import rarfile

            with rarfile.RarFile(input_file) as rar:
                rar.extractall(output_path)
            return
        except ImportError:
            pass

    try:
        _decompress_archive(input_file, output_path)
    except Exception as e:
        utils.error(f"No decompress method for format: `{input_file}` ({str(e)})")


def _decompress_archive(input_file, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

    p7z = shutil.which("7z")
    if p7z != None:
        import subprocess

        p7z_command = [p7z, "x", input_file, "-o" + output_path]
        ret = subprocess.run(p7z_command, capture_output=True, check=False)
        if ret.returncode != 0:
            utils.error("7z decompress failed")

    else:
        try:
            import libarchive

            with libarchive.file_reader(input_file) as archive:
                for entry in archive:
                    target_path = os.path.join(output_path, entry.pathname)

                    if entry.isdir:
                        os.makedirs(target_path, exist_ok=True)
                    else:
                        os.makedirs(os.path.dirname(target_path), exist_ok=True)
                        with open(target_path, "wb") as f:
                            for block in entry.get_blocks():
                                f.write(block)

        except ImportError:
            try:
                import py7zr

                with py7zr.SevenZipFile(input_file, "r") as py7z:
                    py7z.extractall(output_path)

            except ImportError:
                utils.error("Please install `7z` or python module `libarchive`/`py7zr`")


def action(args):
    if args.decompress:
        decompress(args.inpath, args.outpath, args.force)
    elif args.compress:
        compress(args.inpath, args.outpath, args.force)
