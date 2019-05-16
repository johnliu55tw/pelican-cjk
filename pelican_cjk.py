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

PUNC_RANGES = (
    (u'\u3000', u'\u303F'),             # CJK Symbols and Punctuation
    (u'\uFF00', u'\uFFEF'),             # Halfwidth and Fullwidth Forms
)

CJK_PUNC_RANGES = CJK_RANGES + PUNC_RANGES

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


# Patterns for finding the newline character that should removed.
newline_pattern = re.compile(r'({cjk_punc}){newline}(?=({cjk_punc}))'.format(
    cjk_punc=ranges_as_regex(CJK_PUNC_RANGES), newline=os.linesep))

punc_ans_pattern = re.compile(r'({}){}(?=({}))'.format(
    ranges_as_regex(PUNC_RANGES), os.linesep, ranges_as_regex(ANS_RANGES)))

ans_punc_pattern = re.compile(r'({}){}(?=({}))'.format(
    ranges_as_regex(ANS_RANGES), os.linesep, ranges_as_regex(PUNC_RANGES)))


# Patterns for finding CJK and ANS written without space in between.
# The <[^<]*?> is to NOT include more than one tag.
# Noted that the CJK range does not include CJK punctuation.
cjk_ans_pattern = re.compile(r'({})(<[^<]*?>)?({})'.format(
    ranges_as_regex(CJK_RANGES), ranges_as_regex(ANS_RANGES)))

ans_cjk_pattern = re.compile(r'({})(<[^<]*?>)?({})'.format(
    ranges_as_regex(ANS_RANGES), ranges_as_regex(CJK_RANGES)))

# Patterns for finding CJK-tag-CJK
# The <[^<]*?> is to NOT include more than one tag.
cjk_tag_cjk_pattern = re.compile(r'(?<={cjk_punc}) *(<[^<]*?>) *(?={cjk_punc})'.format(
    cjk_punc=ranges_as_regex(CJK_PUNC_RANGES)))


def remove_paragraph_newline(text):
    ret = text

    ret = newline_pattern.sub(r'\1', ret)
    ret = punc_ans_pattern.sub(r'\1', ret)
    ret = ans_punc_pattern.sub(r'\1', ret)

    return ret


def auto_spacing(text):

    def add_space(match):
        """Add the space to the correct place with regards to the match object.
        """
        first_char, tag, second_char = match.groups()
        if tag is None:  # No HTML tag between first and second char
            return first_char + ' ' + second_char
        else:
            if tag.startswith('</'):  # End tag, space should be behind this tag
                return first_char + tag + ' ' + second_char
            else:
                return first_char + ' ' + tag + second_char

    ret = text

    ret = cjk_ans_pattern.sub(add_space, ret)
    ret = ans_cjk_pattern.sub(add_space, ret)

    return ret


def remove_markup_spacing(text):
    return cjk_tag_cjk_pattern.sub(r'\1', text)


def main(content):
    if content._content is None:
        return

    ret = content._content

    if content.settings.get('CJK_REMOVE_PARAGRAPH_NEWLINE', True) is True:
        ret = remove_paragraph_newline(ret)

    if content.settings.get('CJK_AUTO_SPACING', True) is True:
        ret = auto_spacing(ret)

    if content.settings.get('CJK_REMOVE_MARKUP_SPACING', True) is True:
        ret = remove_markup_spacing(ret)

    content._content = ret


def register():
    signals.content_object_init.connect(main)
