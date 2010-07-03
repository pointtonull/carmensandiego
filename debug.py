#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import time
import sys

INICIO = time.time()
VERBOSE = 1

def debug(*args):
    if VERBOSE:
        mensaje = " ".join((str(e) for e in args))
        sys.stderr.write("%7.2f %s\n" % (time.time() - INICIO, mensaje))
