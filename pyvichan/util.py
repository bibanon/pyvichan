#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utility functions."""

import re

# HTMLParser was deprecated since 3.4
try:
    from html import unescape
except ImportError:
    try:
        from html.parser import HTMLParser
    except ImportError:
        from HTMLParser import HTMLParser
    _parser = HTMLParser()
    unescape = _parser.unescape


def clean_comment_body(body):
    """Returns given comment HTML as plaintext.

    Converts all HTML tags and entities within 4chan comments
    into human-readable text equivalents.
    """
    body = unescape(body)
    body = re.sub(r'<a [^>]+>(.+?)</a>', r'\1', body)
    body = body.replace('<br>', '\n')
    body = re.sub(r'<.+?>', '', body)
    return body
