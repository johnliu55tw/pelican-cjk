import re
import unittest
from unittest import mock

import pelican_cjk


class RangesAsRegexTestCase(unittest.TestCase):

    def test_ranges_with_start_and_end(self):
        data = (
            ('a', 'z'),
            ('\u00A0', '\u00AF'),
        )

        re_range = pelican_cjk.ranges_as_regex(data)

        self.assertEqual(re_range, '[a-z\u00A0-\u00AF]')

    def test_ranges_without_end(self):
        data = (
            ('A', ''),
            ('\u00A0\u00A1', ''),
            ('!@#$%', ''),
        )

        re_range = pelican_cjk.ranges_as_regex(data)

        self.assertEqual(re_range, '[A\u00A0\u00A1!@#$%]')

    def test_ranges_mixed(self):
        data = (
            ('A', 'Z'),
            ('\u00A0', ''),
            ('!@#', ''),
            ('a', 'z'),
        )

        re_range = pelican_cjk.ranges_as_regex(data)

        self.assertEqual(re_range, '[A-Z\u00A0!@#a-z]')


class CjkRangeTestCase(unittest.TestCase):

    def is_cjk(self, c):
        return re.match(pelican_cjk.ranges_as_regex(pelican_cjk.CJK_RANGES), c) is not None

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

    def test_newline_removed_if_surrounded_by_CJK(self):
        test_cases = (
            ('你好\n好笑', '你好好笑'),
            ('逗號，\n後面', '逗號，後面'),
            ('（全形括號）\n後面', '（全形括號）後面'),
        )

        for data, answer in test_cases:
            with self.subTest(data=data, answer=answer):
                result = pelican_cjk.remove_paragraph_newline(data)

                self.assertEqual(result, answer)

    def test_newline_kept_if_not_surrounded(self):
        test_cases = (
            '英文abcd\n後面',
            '<some_tag/>\n後面',
            '``literal``\n下一行',
            '`link`_\n下一行',
            '**emph**\n下一行',
            '半形逗號,\n下一行',
            '半形句號.\n下一行',
        )

        for data in test_cases:
            with self.subTest(data=data):
                result = pelican_cjk.remove_paragraph_newline(data)

                self.assertEqual(result, data)


class AutoSpacingTestCase(unittest.TestCase):

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
                result = pelican_cjk.auto_spacing(data)

                self.assertEqual(result, answer)

    def test_with_tag_should_add_space_cases(self):
        test_cases = (
            ('A<em>啥</em>B', 'A <em>啥</em> B'),
            ('中<em>A</em>文', '中 <em>A</em> 文'),
            ('哈哈<em>ABC</em>', '哈哈 <em>ABC</em>'),
            ('ABC<em>哈哈</em>', 'ABC <em>哈哈</em>'),
            ('<strong>ABC</strong>中文', '<strong>ABC</strong> 中文'),
            ('<strong>中文</strong>ABC', '<strong>中文</strong> ABC'),
            ('一<em>2</em>三<em>4</em>', '一 <em>2</em> 三 <em>4</em>'),
            ('<em>1</em>二<em>3</em>四', '<em>1</em> 二 <em>3</em> 四'),
            ('ABC<a href=http://a.b.c>連結</a>CBA', 'ABC <a href=http://a.b.c>連結</a> CBA'),
            ('<em>A</em>NotCJK<em>中文</em>', '<em>A</em>NotCJK <em>中文</em>'),
            ('<em>中</em>是中文<strong>A</strong>', '<em>中</em>是中文 <strong>A</strong>'),
        )

        for data, answer in test_cases:
            with self.subTest(data=data):
                result = pelican_cjk.auto_spacing(data)

                self.assertEqual(result, answer)

    def test_should_not_change_cases(self):
        test_cases = (
            'abcd α£ 1234',
            '哈<some_tag/>啥',
            '中文<p>啥</p>中文',
            '中文 <p>啥</p> 中文',
            'abc <em>def</em> ghi',
            '五&lt;六&gt;七',
            '這&amp;還在',
            'abc。123',
            '123，abc',
        )

        for data in test_cases:
            with self.subTest(data=data):
                result = pelican_cjk.auto_spacing(data)

                self.assertEqual(result, data)

    def test_with_tag_should_not_change_cases(self):
        test_cases = (
            '這是 <strong>中文</strong> 好嗎',
            'ABC <em>ABC</em> ABC',
            'Nested<em><strong>行內</strong></em>Markup',
            '<em>行</em><strong>inside</strong',
        )

        for data in test_cases:
            with self.subTest(data=data):
                result = pelican_cjk.auto_spacing(data)

                self.assertEqual(result, data)


class RemoveMarkupSpacingTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_remove_space_cases(self):
        test_cases = (
            ('中文 <em>中文</em>', '中文<em>中文</em>'),
            ('<em>中文</em> 中文', '<em>中文</em>中文'),
            ('你 <em>好</em> 嗎 <strong>嗨</strong> 嗨',
             '你<em>好</em>嗎<strong>嗨</strong>嗨'),
        )

        for data, answer in test_cases:
            with self.subTest(data=data):
                result = pelican_cjk.remove_markup_spacing(data)

                self.assertEqual(result, answer)

    def test_should_not_change_cases(self):
        test_cases = (
            '中文 中文 中文',
            'ABC <em>中文</em>',
            '<em>中文</em> ABC',
            '中文 <em>ABC</em>',
            '<em>中文</em> ABC',
            '<strong><em>中文</strong></em> 中文'
            '中文 <strong><em>中文</strong></em>'
        )

        for data in test_cases:
            with self.subTest(data=data):
                result = pelican_cjk.remove_markup_spacing(data)

                self.assertEqual(result, data)


@mock.patch('pelican_cjk.remove_markup_spacing')
@mock.patch('pelican_cjk.remove_paragraph_newline')
@mock.patch('pelican_cjk.auto_spacing')
class MainTestCase(unittest.TestCase):

    def setUp(self):
        self.mock_content = mock.MagicMock()
        self.mock_content._content = 'SomeTextThatWillRemainIntact'
        self.mock_content.settings = {'someKey': 'someValue'}

    def tearDown(self):
        pass

    def test_with_default_settings(
            self,
            m_auto_spacing,
            m_remove_newline,
            m_remove_markup_spacing):

        pelican_cjk.main(self.mock_content)

        m_remove_newline.assert_called_with('SomeTextThatWillRemainIntact')
        m_auto_spacing.assert_called_with(m_remove_newline.return_value)
        m_remove_markup_spacing.assert_called_with(m_auto_spacing.return_value)

    def test_with_CJK_REMOVE_PARAGRAPH_NEWLINE_disabled(
            self,
            m_auto_spacing,
            m_remove_newline,
            m_remove_markup_spacing):

        self.mock_content.settings.update({'CJK_REMOVE_PARAGRAPH_NEWLINE': False})

        pelican_cjk.main(self.mock_content)

        m_remove_newline.assert_not_called()
        m_auto_spacing.assert_called_with('SomeTextThatWillRemainIntact')
        m_remove_markup_spacing.assert_called_with(m_auto_spacing.return_value)

    def test_with_CJK_AUTO_SPACING_disabled(
            self,
            m_auto_spacing,
            m_remove_newline,
            m_remove_markup_spacing):

        self.mock_content.settings.update({'CJK_AUTO_SPACING': False})

        pelican_cjk.main(self.mock_content)

        m_remove_newline.assert_called_with('SomeTextThatWillRemainIntact')
        m_auto_spacing.assert_not_called()
        m_remove_markup_spacing.assert_called_with(m_remove_newline.return_value)

    def test_with_REMOVE_CJK_MAKRUP_SPACING_disabled(
            self,
            m_auto_spacing,
            m_remove_newline,
            m_remove_markup_spacing):

        self.mock_content.settings.update({'CJK_REMOVE_MARKUP_SPACING': False})

        pelican_cjk.main(self.mock_content)

        m_remove_newline.assert_called_with('SomeTextThatWillRemainIntact')
        m_auto_spacing.assert_called_with(m_remove_newline.return_value)
        m_remove_markup_spacing.assert_not_called()
