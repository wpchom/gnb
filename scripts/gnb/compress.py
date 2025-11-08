#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from . import error, info

sys.dont_write_bytecode = True

"""
int zip_compress(){}
int zip_decompress(){}

[] = {
    {"zip", zip_compress, zip_decompress},
    {"tar.bz2", bz2_compress, bz2_decompress},
    {"tar.gz", gz_compress, gz_decompress},
}
"""

def _parser_arguments(parser):
    # 创建互斥参数组，使-c和-d参数只能二选一
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--compress", action="store_true", help="compress")
    group.add_argument("-d", "--decompress", action="store_true", help="decompress")

    parser.add_argument("-f", "--format", default=None, help="compress format")
    parser.add_argument("inpath", help="input path")
    parser.add_argument("outpath", help="output path")

def parser(subparsers):
    parser = subparsers.add_parser("compress", aliases=["c"], help="compress or decompress")
    _parser_arguments(parser)

