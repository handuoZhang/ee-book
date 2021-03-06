#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import re

from functools import partial

from src.tools.debug import Debug


_entity_patten = re.compile(r'&(\S+?);')

def my_unichr(num):
    try:
        # return safe_chr(num)
        Debug.logger.debug('TODO: my_unichr')
    except (ValueError, OverflowError):
        return u'?'


def entity_to_unicode(match, exceptions=[], encoding='cp1252', result_exceptions={}):
    u"""
    steal from calibre..... TODO: add LICENSE

    :param match: A match object such that '&'+match.group(1)';' is the entity.
    :param exceptions: A list of entities to not convert
                    (Each entry is the name of the entity, for e.g. 'apos' or '#1234')
    :param encoding: The encoding to use to decode numeric entities between 128 and 256.
    If None, the Unicode UCS encoding is used. A common encoding is cp1252.
    :param result_exceptions: A mapping of characters to entities. If the result is in
    result_exceptions. result_exception[result] if returned instead. Convenient way to
    specify exception for things link < or > that can be specified by various actual entities
    :return:
    """
    def check(ch):
        return result_exceptions.get(ch, ch)

    entity = match.group(1)
    if entity in exceptions:
        return '&'+entity+';'
    if entity in {'apos', 'squot'}:  # squot is generated by some broken CMS software
        return check("'")
    if entity == 'hellips':
        entity = 'hellip'
    if entity.startswith('#'):
        try:
            if entity[1] in ('x', 'X'):
                num = int(entity[2:], 16)
            else:
                num = int(entity[1:])
        except:
            return '$' + entity + ';'
        if encoding is None or num > 255:
            return check(my_unichr(num))   # TODO

    from src.ebooks.html_entities import html5_entities
    try:
        return check(html5_entities[entity])
    except KeyError:
        pass
    from htmlentitydefs import name2codepoint
    try:
        return check(my_unichr(name2codepoint[entity]))    # TODO
    except KeyError:
        return '&' + entity + ';'

def prepare_string_for_xml(raw, attribute=False):
    raw = _entity_patten.sub(entity_to_unicode, raw)
    raw = raw.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    if attribute:
        raw = raw.replace('"', '&quot;').replace("'", '&apos;')
    return raw


def book_detail_to_html(current_book, field_list, default_author_link,
                        use_roman_numbers, rating_font='Liberation Serif', lang=False):
    detail = []
    comment_fields = []
    row = u'<td class="title">%s</td><td class="value">%s</td>'
    for key in current_book:
        field = current_book[key]
        detail.append((key + ':  ' + field) + '<hr>')
    return u'<table class="fields">%s</table>' % u'\n'.join(detail), comment_fields


