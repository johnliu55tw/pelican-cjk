Pelican in CJK
##############

Writting Pelican in Chinese, Japanese and Korean smoothly.

Behavior Changes
****************

Auto spacing
===============

Insert spaces between an half-width (Alphabets, Numbers, Symbols) word
surrounded by CJK charaters.

Before:
   中間的English Vocabulary很Beautiful。

After:
   中間的 English Vocabulary 單字很 Beautiful。

Noted that f the neighbor CJK character is a **punctuation**, space will not be
added:

- 我會說 English。
- 你如果 Happy，I am happy too。

Known exceptions
----------------

This plugin works on the HTML data without any HTML parser, so there are some
limitations on auto spacing in several rarely used scenarios:


1. If the word is in **nested** inline markup, no space will be added around
   it. This is not possible in reStructuredText, so only Markdown users will be
   affected. Examples (in HTML):

   - ``Nested<em><strong>行內</strong><em>Markup``: Spaces should be added
     between **Nested**, **行內** and **Markup**. But since **行內** is in
     nested Markup, spaces won't be added.

2. A word in an inline markup immediately after another inline markup will not
   be adjusted. Examples:

   - **粗體**\ *italic*
   - **程式**\ ``foo_bar = 'nice'``\ *寫的不錯*


Remove newline for CJK paragraph
===================================

Newline characters in a paragraph will be kept in the output HTML. Browser will
then interpret this newline character as a **space**. This is fine in English,
but it looks weird in CJK. This plugin solve this problem by removed a newline
character surrounded by CJK characters.

Before:
   這是第一行
   和第二行

After:
   這是第一行和第二行

Usage
*****

Add this plugin to your ``pelicanconf.py``. Refer to
`pelican-plugins <https://github.com/getpelican/pelican-plugins>`_ for
more details::

   PLUGINS = ['pelican_cjk']

   # Change the default the behavior
   CJK_AUTO_SPACING = False
   ...

These variables can be used to control the behavior:

``CJK_AUTO_SPACING``
   Set to ``False`` to disable `Auto spacing`_. Default to ``True``.

``CJK_REMOVE_PARAGRAPH_NEWLINE``
   Set to ``False`` to disable `Remove newline for CJK paragraph`_.
   Default to ``True``.
