import os
import re
import unittest

import pelican_cjk_correct_spaces as plugin


def read_test_data(filename):
    full_path = os.path.join(
        os.path.dirname(__file__),
        'testdata',
        filename)

    with open(full_path) as f:
        return f.read()


CJK_WITH_NEWLINES = read_test_data('cjk_with_newlines.html')
ENG_WITH_NEWLINES = read_test_data('eng_with_newlines.html')


class RangesAsReTestCase(unittest.TestCase):

    def test_search_found(self):
        p = re.compile(plugin.cjk_regex_range())

        result = p.search('abcd\U0002A701efgh')

        self.assertEqual(result.start(), 4)
        self.assertEqual(result.end(), 5)

    def test_search_not_found(self):
        p = re.compile(plugin.cjk_regex_range())

        result = p.search('abcd\uA000efgh')

        self.assertIsNone(result)


class CjkRangeTestCase(unittest.TestCase):

    def is_cjk(self, c):
        return re.match(plugin.cjk_regex_range(), c) is not None

    def test_pattern_matched(self):
        self.assertTrue(self.is_cjk('我'))
        self.assertTrue(self.is_cjk('あ'))
        self.assertTrue(self.is_cjk('マ'))
        self.assertTrue(self.is_cjk('한'))
        self.assertTrue(self.is_cjk('목'))
        self.assertTrue(self.is_cjk('ㄱ'))

    def test_pattern_not_matched(self):
        self.assertFalse(self.is_cjk('a'))
        self.assertFalse(self.is_cjk('Ā'))
        self.assertFalse(self.is_cjk('ŝ'))
        self.assertFalse(self.is_cjk('>'))
        self.assertFalse(self.is_cjk('!'))
        self.assertFalse(self.is_cjk('\n'))


class RemoveNewlineTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_remove_newline_if_surrounded_by_CJK(self):
        result = plugin.remove_newline_spaces(CJK_WITH_NEWLINES)

        self.assertIn('第一段第一行第二行', result)

    def test_not_remove_newline_if_not_surrounded(self):
        result = plugin.remove_newline_spaces(ENG_WITH_NEWLINES)

        self.assertIn('First line,\nsecond line', result)
