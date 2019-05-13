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


class RangesAsRegexTestCase(unittest.TestCase):

    def test_ranges_with_start_and_end(self):
        data = (
            ('a', 'z'),
            ('\u00A0', '\u00AF'),
        )

        re_range = plugin.ranges_as_regex(data)

        self.assertEqual(re_range, '[a-z\u00A0-\u00AF]')

    def test_ranges_without_end(self):
        data = (
            ('A', ''),
            ('\u00A0\u00A1', ''),
            ('!@#$%', ''),
        )

        re_range = plugin.ranges_as_regex(data)

        self.assertEqual(re_range, '[A\u00A0\u00A1!@#$%]')

    def test_ranges_mixed(self):
        data = (
            ('A', 'Z'),
            ('\u00A0', ''),
            ('!@#', ''),
            ('a', 'z'),
        )

        re_range = plugin.ranges_as_regex(data)

        self.assertEqual(re_range, '[A-Z\u00A0!@#a-z]')


class CjkRangeTestCase(unittest.TestCase):

    def is_cjk(self, c):
        return re.match(plugin.ranges_as_regex(plugin.CJK_RANGES), c) is not None

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


class AddSpaceTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_add_space_cases(self):
        test_cases = (
            ('哈哈ABC', '哈哈 ABC'),
            ('ABC中文', 'ABC 中文'),
            ('哈哈##@@嘻嘻', '哈哈 ##@@ 嘻嘻'),
            ('一2三4', '一 2 三 4'),
            ('1二3四', '1 二 3 四'),
            ('這是α', '這是 α'),
            ('這是£', '這是 £'),
            ('這是=', '這是 ='),
        )

        for data, answer in test_cases:
            with self.subTest(data=data, answer=answer):
                result = plugin.add_space(data)

                self.assertEqual(result, answer)

    def test_should_not_change_cases(self):
        test_cases = (
            'abcd α£ 1234',
            '哈<some_tag/>啥',
            '中文<p>啥</p>中文',
            '中文 <p>啥</p> 中文',
            '五&lt;六&gt;七',
            '這&amp;還在',
            'abc。123',
            '123，abc',
        )

        for data in test_cases:
            with self.subTest(data=data):
                result = plugin.add_space(data)

                self.assertEqual(result, data)
