#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.dont_write_bytecode = True

if len(sys.argv) < 2:
    sys.stderr.write("Usage: which.py <command>\n")
    sys.exit(1)

for arg in sys.argv[1:]:
    import shutil

    w = shutil.which(arg)
    if w:
        sys.stdout.write(os.path.abspath(w))
        sys.exit(0)

sys.stdout.write("")
