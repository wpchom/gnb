#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
from . import utils

sys.dont_write_bytecode = True


def _parser_arguments(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--compress", action="store_true", help="compress")
    group.add_argument("-d", "--decompress", action="store_true", help="decompress")

    parser.add_argument("-f", "--format", default=None, help="compress format")
    parser.add_argument("inpath", help="input path")
    parser.add_argument("outpath", help="output path")


def parser(subparsers):
    parser = subparsers.add_parser(
        "compress", aliases=["e"], help="compress or decompress"
    )
    _parser_arguments(parser)


def compress(input_path, output_file, force):
    pass


def decompress(input_file, output_path, force):
    if output_path == None:
        output_path = os.path.dirname(input_file)

    if os.path.exists(output_path):
        if force:
            shutil.rmtree(output_path)
        else:
            utils.error(f"output directory already exists: {output_path}")

    if (input_file.split(".")[-2] in ["tar"]) or (
        input_file.split(".")[-1] in ["tgz", "tbz2", "txz"]
    ):
        import tarfile

        tarfile.open(input_file).extractall(output_path)
        return

    elif input_file.split(".")[-1] in ["zip"]:
        import zipfile

        zipfile.ZipFile(input_file).extractall(output_path)
        return

    elif input_file.split(".")[-1] in ["rar"]:
        try:
            import rarfile

            rarfile.RarFile(input_file).extractall(output_path)
            return

        except ImportError:
            pass

    try:
        _decompress_archive(input, output_path)
    except Exception as e:
        utils.error(f"no decompress method for format: {input_file} ({str(e)})")


def _decompress_archive(input, output):
    if not os.path.exists(output):
        os.makedirs(output, exist_ok=True)

    p7z = shutil.which("7z")
    if p7z != None:
        import subprocess

        p7z_command = [p7z, "x", input, "-o", output]
        ret = subprocess.run(p7z_command, cwd=output, check=False)
        if ret.returncode != 0:
            utils.error("7z decompress failed")

    else:
        try:
            import libarchive

            with libarchive.file_reader(input) as archive:
                for entry in archive:
                    target_path = os.path.join(output, entry.pathname)

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

                py7z = py7zr.SevenZipFile(input, "r")
                py7z.extractall(output)
                py7z.close()

            except ImportError:
                utils.error("please install `7z` or python module `libarchive`/`py7zr`")
