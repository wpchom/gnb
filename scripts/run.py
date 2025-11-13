#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess

sys.dont_write_bytecode = True

if len(sys.argv) < 2:
    sys.stderr.write("Usage: run.py <command> [args...]\n")
    sys.exit(1)

try:
    ret = subprocess.run(sys.argv[1:])
    sys.exit(ret.returncode)
except KeyboardInterrupt:
    sys.stderr.write("\nInterrupted\n")
    sys.exit(1)
except Exception as e:
    sys.stderr.write(f"Error: {str(e)}\n")
    sys.exit(1)
