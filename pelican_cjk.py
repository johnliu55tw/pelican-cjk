import os
import re

from pelican import signals


def ranges_as_regex(ranges):
    pattern_text = '['
    for start, end in ranges:
        if end == '':
            pattern_text += start
        else:
            pattern_text += '{}-{}'.format(start, end)
    pattern_text += ']'

    return pattern_text


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
    (u'\u3040', u'\u309F'),             # Hiragana
    (u'\u30A0', u'\u30FF'),             # Katakana
    (u'\u4E00', u'\u9FAF'),             # CJK unified Ideographs
    # References: https://en.wikipedia.org/wiki/Korean_language_and_computers#Hangul_in_Unicode
    (u'\uAC00', u'\uD7A3'),             # Hangul Syllables
    (u'\u1100', u'\u11FF'),             # Hangul Jamo
    (u'\u3130', u'\u318F'),             # Hangul Compatibility Jamo
    (u'\uA960', u'\uA97F'),             # Hangul Jamo Ext. A
    (u'\uD7B0', u'\uD7FF'),             # Hangul Jamo Ext. B
)

CJK_PUNC_RANGES = CJK_RANGES + (
    (u'\u3000', u'\u303F'),             # CJK Symbols and Punctuation
    (u'\uFF00', u'\uFFEF'),             # Halfwidth and Fullwidth Forms
)

# Alphabets, Numbers and Symbols
ANS_RANGES = (
    ('a', 'z'),
    ('A', 'Z'),
    ('0', '9'),
    ("'", ''),                          # Single quote
    (r'`~@#%"/_=,:\!\$\^\*\(\)\-\+\[\]\{\}\\\|\.\?', ''),  # Characters <>&;' are removed
    (u'\u00A1', u'\u00FF'),
    (u'\u0370', u'\u03FF'),             # Greek and Coptic
)


newline_pattern = re.compile(r'({cjk_punc}){newline}(?=({cjk_punc}))'.format(
    cjk_punc=ranges_as_regex(CJK_PUNC_RANGES), newline=os.linesep))

cjk_ans_pattern = re.compile(r'({})({})'.format(
    ranges_as_regex(CJK_RANGES), ranges_as_regex(ANS_RANGES)))

ans_cjk_pattern = re.compile(r'({})({})'.format(
    ranges_as_regex(ANS_RANGES), ranges_as_regex(CJK_RANGES)))


def remove_paragraph_newline(text):
    return newline_pattern.sub(r'\1', text)


def auto_spacing(text):
    ret = text

    ret = cjk_ans_pattern.sub(r'\1 \2', ret)
    ret = ans_cjk_pattern.sub(r'\1 \2', ret)

    return ret


def main(content):
    if content._content is None:
        return

    ret = content._content

    if content.settings.get('CJK_REMOVE_PARAGRAPH_NEWLINE', True) is True:
        ret = remove_paragraph_newline(ret)

    if content.settings.get('CJK_AUTO_SPACING', True) is True:
        ret = auto_spacing(ret)

    content._content = ret


def register():
    signals.content_object_init.connect(main)
