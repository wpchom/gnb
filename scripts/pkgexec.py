#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys

sys.dont_write_bytecode = True

if len(sys.argv) < 2:
    sys.stderr.write("Usage: which.py <command>\n")
    sys.exit(1)

os.system(" ".join([str(arg) for arg in sys.argv[1:]]))
