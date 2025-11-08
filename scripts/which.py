#!/usr/bin/python3

import os
import sys
import shutil

sys.dont_write_bytecode = True

for arg in sys.argv[1:]:
    w = shutil.which(arg)
    if w:
        sys.stdout.write(os.path.abspath(w))
        exit(0)

sys.stdout.write("")
