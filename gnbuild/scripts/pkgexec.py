#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess

sys.dont_write_bytecode = True

if len(sys.argv) < 2:
    sys.stderr.write("Usage: which.py <command>\n")
    sys.exit(1)

subprocess.run(" ".join(sys.argv[1:]), shell=True, check=True)
