#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import time
import sys

INICIO = time.time()
VERBOSE = 1

def debug(*args):
    if VERBOSE:
        mensaje = " ".join((repr(e) for e in args))
        try:
            sys.stderr.write("%7.2f %s\n" % (time.time() - INICIO, mensaje.decode("latin-1")))
        except:
            pass
