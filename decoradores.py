#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import pickle
import sys
import os
import time
import signal
import inspect

try:
    from multiprocessing import Queue, Process
    MP = True
except ImportError:
    MP = False

from debug import debug
from functools import wraps
from threading import Thread


VERBOSE = False

class Asyncobj(Thread):
    def __init__(self, func, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.func = func
        Thread.__init__(self)
        self.result = None


    def __call__(self):
        return self


    def is_alive(self):
        try:
            return Thread.is_alive(self)
        except AttributeError:
            return Thread.isAlive(self)


    def run(self):
        self.result = self.func(*self.args, **self.kwargs)

    def get_result(self, timeout=None):
        self.join(timeout)
        return self.result


class Async:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kw):
        func = Asyncobj(self.func, *args, **kw)
        func.start()
        return func

    def __repr__(self):
        return self.func.func_name


def nothreadsafe(func):

    def container(queue, *args, **kwargs):
        queue.put(func(*args, **kwargs))

    @wraps(func)
    def dfunc(*args, **kwargs):
        queue = Queue()

        proc = Process(None, container, None, (queue,) + args, kwargs)

        proc.start()
        proc.join()
        return queue.get()

    return dfunc


def Indeterminado(fallback=0):
    def decorador(funcion):
        def decorada(*args, **kwargs):
            try:
                result = funcion(*args, **kwargs)
            except RuntimeError:
                result = 0
            return result

        return decorada

    return decorador


class TimeoutExc(Exception):
    def __init__(self, value="Timed Out"):
        debug("Time out ¬¬")
        Exception.__init__(self)
        self.value = value

def mptimeout(timeout, func, *args, **kwargs):
    assert inspect.isfunction(func) or inspect.ismethod(func)

    @wraps(func)
    def newfunc(queue, args, kwargs):
        return queue.put(func(*args, **kwargs))

    queue = Queue()
    proc = Process(None, newfunc, newfunc.func_name,
        (queue, args, kwargs))
    proc.start()
    proc.join(timeout)

    try:
        return queue.get()
    except:
        return None

#    if proc.is_alive():
#        proc.terminate()
#        raise TimeoutExc()
#    else:
#        return queue.get()

def signaltimeout(timeout, func, *args, **kwargs):
    def handler(snum, frame):
        raise TimeoutExc

    old = signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)

    try:
        result = func(*args, **kwargs)
    finally:
        signal.signal(signal.SIGALRM, old)

    signal.alarm(0)

    return result


def Timeout(time, default=None):
    def decorator(func):
        def decorated(*args, **kwargs):

            try:
                if MP:
                    return mptimeout(time, func, *args, **kwargs)
                else:
                    return signaltimeout(time, func, *args, **kwargs)
            except TimeoutExc:
                return default

        return decorated

    return decorator


class Mono:
    def __init__(self, func):
        self.func = func
        self.running = False

    def __call__(self, *args, **kw):
        if self.running:
            debug("Mono: bleh!")
            return None
        else:
            self.running = True
            result = self.func(*args, **kw)
            self.running = False
            return result


class FunctionList(dict):
    def __call__(self, func):
        self.__setitem__(func.__name__, func)
        return func


class Cache:
    def __init__(self, limite=100 * 86400, ruta=None, flush_frequency=1):
        self.count = 0
        self.limite = limite
        self.ruta = ruta
        self.flush_frequency = flush_frequency

        if ruta:
            try:
                f = open(self.ruta, "rb")
                self.cache = pickle.load(f)
                f.close()
            except IOError:
                self.cache = {}
            except EOFError:
                self.cache = {}
        else:
            self.cache = {}

    def __call__(self, func):
        @wraps(func)
        def call(*args, **kw):
            r = self.cache.get(args, None)
            if r and time.time() - r[0] < self.limite:

                if VERBOSE: debug(" Cache load: %s %s %s : %s" % (
                    func.func_name,
                    args,
                    kw,
                    r[1],
                    ))

                return r[1]

            else:
                if VERBOSE: debug(" Cache: No load")
                r = time.time(), func(*args, **kw)

                if r[1] is not None:
                    self.cache[args] = r
                self.count += 1

                if VERBOSE: debug(" Cache save: %s %s %s : %s" % (
                    func.func_name,
                    args,
                    kw,
                    r[1],
                    ))

                if self.count % self.flush_frequency == 0:
                    self.flush()

                return r[1]

        return call

    def flush(self):

        if self.ruta:
            try:
                f = open(self.ruta, "rb")
                self.cache = pickle.load(f)
                f.close()
            except:
                if VERBOSE: debug("Error en lectura del cache")
            f = open(self.ruta, "wb")
            pickle.dump(self.cache, f, -1)
            f.flush()
            f.close()
            if VERBOSE: debug("Cache escrito exitosamente en %s" % self.ruta)


class Timeit:

    def __init__(self, function):
        self.function = function
        self.totaltime = 0
        self.totalcalls = 0

    def __call__(self, *args, **kw):
        start = time.time()
        result = self.function(*args, **kw)
        timeit = time.time() - start
        self.totaltime += timeit
        self.totalcalls += 1
        if VERBOSE: debug(" Time: %s %s %s : %s  %.2f (%.2f)" % (
            self.function.func_name,
            args,
            kw,
            result,
            timeit,
            self.totaltime / self.totalcalls,
            ))
        return result


class Retry:

    def __init__(self, attempts=5, retry_on=None, pause=5):
        self.attempts = attempts
        self.retry_on = retry_on
        self.pause = pause

    def __call__(self, func):
        def call(*args, **kwargs):
            for attempt in xrange(self.attempts):
                result = func(*args, **kwargs)

                if result != self.retry_on:
                    return result

                if VERBOSE:
                    debug(" Retry %d: %s(*%s)" % (attempt, func.func_name,
                        args))
                time.sleep(self.pause)
            else:
                debug(" Failed %s(*%s, **%s)" % (func.func_name, args, kwargs))

            return result
        return call


def get_depth():
    def exist_frame(n):
        try:
            if sys._getframe(n):
                return True
        except ValueError:
            return False

    now = 0
    maxn = 1
    minn = 0

    while exist_frame(maxn):
        minn = maxn
        maxn *= 2

    # minn =< depth < maxn
    middle = (minn + maxn) / 2

    while minn < middle:
        if exist_frame(middle):
            minn = middle
        else:
            maxn = middle

        middle = (minn + maxn) / 2

    return max(minn - 4, 0) #4 == len(main, module, Verbose, get_depth)

def relpath(path):
    return os.path.abspath(path).replace(os.path.commonprefix(
        (os.path.abspath(os.path.curdir), os.path.abspath(path))), "")

def Verbose(calling=1, returning=0):

    def decorador(func):
        @wraps(func)
        def dfunc(*args, **kwargs):

            if calling > 1:
                debug("%s> %s(%s, %s)" % (" " * get_depth(), func.func_name,
                    args, kwargs))
            elif calling > 0:
                debug("%s> %s" % (" " * get_depth(), func.func_name))

            result = func(*args, **kwargs)

            if returning > 2:
                debug('%s< %s, file "%s", line %s' % (" " * get_depth(),
                    func.func_name, relpath(inspect.getfile(func)),
                    inspect.getsourcelines(func)[-1]))
            elif returning > 1:
                debug("%s< %s: %s" % (" " * get_depth(), func.func_name,
                    result))
            elif returning > 0:
                debug('%s< %s' % (" " * get_depth(), func.func_name))

            return result

        return dfunc
    return decorador

def Deprecated(level=1):
    """
Level can be 0 (do nothing), 1 (print debug waring) o 2 (raise
DeprecationWarning)
    """

    assert level in (0, 1, 2)

    def decorator(func):

        @wraps(func)
        def dfunc(*args, **kwargs):
            if level > 0:
                debug(" W: Usind deprecated %s from %s" % (func.func_name,
                    inspect.getfile(func)))

            if level == 2:
                raise DeprecationWarning("""Busted!""")

            return func(*args, **kwargs)

        return dfunc

    return decorator


class MetaSingleton(type):

    def __init__(self, name, bases, dict):
        """
Singleton Metaclass. You must use it on the __metaclass__ class atribute.
        """
        super(MetaSingleton, self).__init__(name, bases, dict)
        self.instance = None

    def __call__(self, *args, **kw):
        if self.instance is None:
            self.instance = super(MetaSingleton, self).__call__(*args, **kw)

        return self.instance


class Singleton(object):
    """Just an example."""
    __metaclass__ = MetaSingleton


def main():

    @Cache
    def fibonar(n):
        if n < 2: return n
        else: return fibonar(n - 1) + fibonar(n - 2)


    print(fibonar(500))

if __name__ == "__main__":
    exit(main())
