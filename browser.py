#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import os
import webbrowser
import time
import ClientForm
import cPickle

from tempfile import mkdtemp
from debug import debug
from decoradores import signaltimeout
from cStringIO import StringIO

from urllib2 import URLError

import twill
from twill.utils import BrowserStateError

tc = twill.commands
twill.set_output(StringIO())
twill.commands.config("use_tidy", 0)

TEMPDIR = mkdtemp()
HOME = os.environ["HOME"]
CACHE = HOME +  "/.browser_cache"

class FORM(object):

    def __init__(self, parent, form):
        self.parent = parent
        self._form = form
        self.names = [control.name for control in self._form.controls]

    def click_request_data(self):
        return self._form.click_request_data()

    def __getitem__(self, y):
        return self._form.__getitem__(y)

    def __setitem__(self, i, y):
        return self._form.__setitem__(i, y)

    def __repr__(self):
        return str(self.names)

    def __str__(self):
        return self._form.__str__()

    def click(self):
        return self._form.click()

    def submit(self, *args, **kw):
        return self.parent.put_form(self, *args, **kw)

    def set_all_readonly(self, *args, **kw):
        return self._form.set_all_readonly(*args, **kw)


class BROWSER:

    def __init__(self, timeout=120):

        self._twillbrowser = tc.get_browser()
        self._twillbrowser.set_agent_string("moz7")
        self.timeout = timeout

        self.htmlCache = None

    def reload(self):
        return self._twillbrowser.reload()

    def show(self, url=None, openon=None):
        if url:
            self.go(url)
        temppath = "%s/%d.html" % (TEMPDIR, time.time())
        tempfile = open(temppath, "w")
        tempfile.write(self.get_html())
        tempfile.close()
        debug(temppath)

        if not openon:
            return webbrowser.open(temppath)
        else:
            return webbrowser.GenericBrowser(openon).open(temppath)

    def clear_cookies(self):
        return self._twillbrowser.clear_cookies()

    def add_cookie(self, cookie, dominio):
        """Por ahora no se me ocurrió un metodo más elegante..."""
        temppath = "%s/%d" % (TEMPDIR, time.time())
        self._twillbrowser.save_cookies(temppath)
        cookiefile = open(temppath, "a+")
        cookiefile.write("""Set-Cookie3:%s; path="/";domain="%s";path_spec;"""
            """domain_dot; expires""; version=0""" % (cookie, dominio))
        cookiefile.close()
        self._twillbrowser.load_cookies(temppath)

    def go(self, url):
        try:
            #TODO: Re-implement TimeOut
            signaltimeout(self.timeout, self._twillbrowser.go, url)
        except ValueError:
            self._twillbrowser.go(url)

        return self.get_code(), self.get_title()

    def get_html(self, url=None, *args, **kw):
        cache = kw.get("cache", 0)

        if cache is 0:
            if url:
                self.go(url)
            html = self._twillbrowser.get_html()
        else:
            html = self.get_html_from_cache(url, cache)


        return html


    def get_html_from_cache(self, url, cache):
        if self.htmlCache is None:
            try:
                self.htmlCache = cPickle.load(open(CACHE))
            except IOError:
                self.htmlCache = {}

        date, html = self.htmlCache.get(url, (0, ""))

        if (time.time() - date) > cache:
            self.go(url)
            html = self._twillbrowser.get_html()
            date = time.time()
            self.htmlCache[url] = date, html
            cPickle.dump(self.htmlCache, open(CACHE, "w"), -1)

        return html



    def get_title(self, url=None, *args, **kwargs):
        if url:
            self.go(url, *args, **kwargs)
        return self._twillbrowser.get_title()

    def get_code(self, url=None):
        if url:
            self.go(url)
        return self._twillbrowser.get_code()

    def get_url(self):
        return self._twillbrowser.get_url()

    def get_forms(self, url=None, *args, **kw):

        if url is None:
            url = self.get_url()

        fifo = StringIO()
        fifo.writelines(self.get_html(url, *args, **kw))
        fifo.seek(0)
        forms = ClientForm.ParseFile(fifo, url, backwards_compat=False)

        return [FORM(self, form) for form in forms]

    def put_form(self, form=None, *args, **kw):
        if form is None:
            # Por compactibilidad con versiones anteriores
            self._twillbrowser.submit()
        else:
            code = 200
            try:
                response = self._twillbrowser._browser.open(
                    form._form.click(*args, **kw))
            except URLError, e:
                debug("Error: %s" % e)
                try:
                    code = int(e)
                except TypeError:
                    code = 404
                    html = ""
                    url = ""
            else:
                html = "\n".join(response.readlines())
                url = response.geturl()

            self._twillbrowser.result = twill.utils.ResultWrapper(
                200, url, html)

        return self.get_code(), self.get_title()


def main():
    print """Este programa está diseñado para ser usado como modulo"""


if __name__ == "__main__":
    exit(main())
