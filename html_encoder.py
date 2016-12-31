# -*- coding: utf-8 -*-

import sys
import sublime
import sublime_plugin

PY_MAJOR_VER = sys.version_info[0]
PY_MINOR_VER = sys.version_info[1]


class HtmlDecodeCommand(sublime_plugin.TextCommand):

    def decode_html(self, str):
        # Use unescape from py standard lib
        # see: http://stackoverflow.com/questions/2087370
        if PY_MAJOR_VER == 2:
            # python 2
            from HTMLParser import HTMLParser
            return HTMLParser().unescape(str)
        elif PY_MAJOR_VER == 3 and PY_MINOR_VER <= 3:
            # python 3
            from html.parser import HTMLParser
            return HTMLParser().unescape(str)
        else:
            # python 3.4+
            from html import unescape
            return unescape(str)

    def selections(self, view, default_to_all=True):
        regions = [r for r in view.sel() if not r.empty()]
        if not regions and default_to_all:
            regions = [sublime.Region(0, view.size())]
        return regions

    def run(self, edit):
        view = self.view
        source_text = decoded_text = ''

        for region in self.selections(view):
            source_text = decoded_text = view.substr(region)
            if len(source_text) > 0:
                decoded_text = self.decode_html(source_text)

        if source_text == decoded_text:
            sublime.set_timeout(lambda: sublime.status_message('HTML Encoder: Nothing to decode.'), 0)
        else:
            view.replace(edit, region, decoded_text)
            sublime.set_timeout(lambda: sublime.status_message('HTML Encoder: HTML Decoded.'), 0)


class HtmlEncodeCommand(sublime_plugin.TextCommand):

    def encode_html(self, str):
        if PY_MAJOR_VER >= 3:
            from html import escape
            return escape(str)
        else:
            # use saxutils escape for python 2
            from xml.sax.saxutils import escape
            html_escape_table = {'"': "&quot;", "'": "&apos;"}
            str = escape(str, html_escape_table)
            str = str.decode('utf-8')
            str = str.encode('ascii', 'xmlcharrefreplace')
            return str

    def selections(self, view, default_to_all=True):
        regions = [r for r in view.sel() if not r.empty()]
        if not regions and default_to_all:
            regions = [sublime.Region(0, view.size())]
        return regions

    def run(self, edit):
        view = self.view
        source_text = encoded_text = ''

        for region in self.selections(view):
            source_text = encoded_text = view.substr(region)
            if len(source_text) > 0:
                encoded_text = self.encode_html(source_text)

        if source_text == encoded_text:
            sublime.set_timeout(lambda: sublime.status_message('HTML Encoder: Nothing to encode.'), 0)
        else:
            view.replace(edit, region, encoded_text)
            sublime.set_timeout(lambda: sublime.status_message('HTML Encoder: HTML Encoded.'), 0)
