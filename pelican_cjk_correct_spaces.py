import os
import re
import logging

from pelican import signals


CJK_RANGES = (
    # References: https://en.wikipedia.org/wiki/CJK_Unified_Ideographs
    (u'\u4E00', u'\u9FFF'),             # CJK Unified Ideographs
    (u'\u3400', u'\u4DBF'),             # CJK Unified Ideographs Ext. A
    (u'\U00020000', u'\U0002A6DF'),     # CJK Unified Ideographs Ext. B
    (u'\U0002A700', u'\U0002B73F'),     # CJK Unified Ideographs Ext. C
    (u'\U0002B740', u'\U0002B81F'),     # CJK Unified Ideographs Ext. D
    (u'\U0002B820', u'\U0002CEAF'),     # CJK Unified Ideographs Ext. E
    (u'\U0002CEB0', u'\U0002EBEF'),     # CJK Unified Ideographs Ext. F
    (u'\uF900', u'\uFAFF'),             # CJK Compatibility Ideographs
    (u'\U0002F800', u'\U0002FA1F'),     # CJK Compatibility Ideographs Supplement
    # References: https://stackoverflow.com/a/30200250
    (u'\u3000', u'\u303F'),             # Japanese-style punctuation
    (u'\u3040', u'\u309F'),             # Hiragana
    (u'\u30A0', u'\u30FF'),             # Katakana
    (u'\uFF00', u'\uFFEF'),             # Full-width roman characters and half-width katakana
    (u'\u4E00', u'\u9FAF'),             # CJK unified Ideographs
    # References: https://en.wikipedia.org/wiki/Korean_language_and_computers#Hangul_in_Unicode
    (u'\uAC00', u'\uD7A3'),             # Hangul Syllables
    (u'\u1100', u'\u11FF'),             # Hangul Jamo
    (u'\u3130', u'\u318F'),             # Hangul Compatibility Jamo
    (u'\uA960', u'\uA97F'),             # Hangul Jamo Ext. A
    (u'\uD7B0', u'\uD7FF'),             # Hangul Jamo Ext. B
)


def cjk_regex_range():
    pattern_text = '['
    for start, end in CJK_RANGES:
        pattern_text += '{}-{}'.format(start, end)
    pattern_text += ']'

    return pattern_text


newline_pattern = re.compile(r'{}({})'.format(os.linesep, cjk_regex_range()))


def remove_newline_spaces(text):
    return newline_pattern.sub(r'\1', text)


def main(content):
    if content._content is None:
        return

    content._content = remove_newline_spaces(content._content)


def register():
    signals.content_object_init.connect(main)
