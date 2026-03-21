#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import shutil

sys.dont_write_bytecode = True

if len(sys.argv) != 3:
    sys.stderr.write("Usage: copy.py <src> <dst>\n")
    sys.exit(1)

shutil.copytree(sys.argv[1], sys.argv[2], dirs_exist_ok=True)
