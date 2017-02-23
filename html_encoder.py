# -*- coding: utf-8 -*-

import sys
import sublime
import sublime_plugin

PY_MAJOR_VER = sys.version_info[0]
PY_MINOR_VER = sys.version_info[1]


def selections(view, default_to_all=True):
    regions = [r for r in view.sel() if not r.empty()]
    if not regions and default_to_all:
        regions = [sublime.Region(0, view.size())]
    return regions


def encode_html(txt):
    if PY_MAJOR_VER >= 3:
        from html import escape
        return escape(txt)
    else:
        # use saxutils escape for python 2
        from xml.sax.saxutils import escape
        html_escape_table = {'"': "&quot;", "'": "&apos;"}
        txt = escape(txt, html_escape_table)
        txt = txt.decode('utf-8')
        txt = txt.encode('ascii', 'xmlcharrefreplace')
        return txt


def decode_html(txt):
    # Use unescape from py standard lib
    # see: http://stackoverflow.com/questions/2087370
    if PY_MAJOR_VER == 2:
        # python 2
        from HTMLParser import HTMLParser
        return HTMLParser().unescape(txt)
    elif PY_MAJOR_VER == 3 and PY_MINOR_VER <= 3:
        # python 3
        from html.parser import HTMLParser
        return HTMLParser().unescape(txt)
    else:
        # python 3.4+
        from html import unescape
        return unescape(txt)


class HtmlDecodeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        file_changed = False

        for region in selections(view):
            source = view.substr(region)
            transformed = decode_html(source)
            if source != transformed:
                view.replace(edit, region, transformed)
                file_changed = True

        if file_changed is True:
            sublime.set_timeout(lambda: sublime.status_message(
                'HTML Encoder: HTML Decoded.'), 0)
        else:
            sublime.set_timeout(lambda: sublime.status_message(
                'HTML Encoder: Nothing to decode.'), 0)


class HtmlEncodeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        file_changed = False

        for region in selections(view):
            source = view.substr(region)

            # decode first to prevent double-encoding:
            source_decoded = decode_html(source)

            transformed = encode_html(source_decoded)
            if source != transformed:
                view.replace(edit, region, transformed)
                file_changed = True

        if file_changed is True:
            sublime.set_timeout(lambda: sublime.status_message(
                'HTML Encoder: HTML Encoded.'), 0)
        else:
            sublime.set_timeout(lambda: sublime.status_message(
                'HTML Encoder: Nothing to encode.'), 0)
