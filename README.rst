Pelican in CJK
##############

Writing Pelican in Chinese, Japanese, and Korean smoothly.


Behavior Changes
****************


Remove newline for CJK paragraph
===================================

Newline characters in a paragraph will be kept in the output HTML, then browser
will interpret this newline character as a **space** character. This is fine in
English, but it looks weird in CJK. These newline characters will be removed.

Before:
   這是第一行
   和第二行

After:
   這是第一行和第二行

Also, if one of the characters surrounding the newline character is
punctuation, it will also be removed.

Before:
   句號。
   English

After:
   句號。English


Auto spacing
===============

Insert spaces between a half-width (Alphabets, Numbers, Symbols) word
surrounded by CJK characters.

Before:
   中間的English Vocabulary單字很Beautiful。

After:
   中間的 English Vocabulary 單字很 Beautiful。

Noted that if the neighbor CJK character is **punctuation**, space will not
be added:

- 我會說 English。
- 你如果 Happy，I am happy too。

Known exceptions and notices
----------------------------

Auto spacing works on the HTML data without any HTML parser. For simplicity,
some less used scenarios are worth noticing:

1. The **title of an article** cannot be changed using the HTML data,
   so it will not be adjusted.

2. If the word is in **nested** inline markup, no space will be added around
   it. This is not possible in reStructuredText, so only Markdown users will be
   affected. Examples (in HTML):

   - ``Nested<em><strong>行內</strong><em>Markup``: Spaces should be added
     between **Nested**, **行內** and **Markup**. But since **行內** is in
     nested Markup, spaces won't be added.

3. A word in an inline markup immediately after another inline markup will not
   be adjusted. Examples:

   - **粗體**\ *italic*
   - **程式**\ ``foo_bar = 'nice'``\ *寫的不錯*

4. Text in
   `literal block <http://docutils.sourceforge.net/docs/user/rst/quickref.html#literal-blocks>`_
   will also be adjusted. Try not to mix CJK and English in this block.


Remove spacing around inline markups
====================================

This is mainly for reStructuredText since it requires a space before and after
an inline markup. Because this is more aggressive behavior, it's separated
from `Auto spacing`_ which you can disable independently.

Before:
   中文的 **粗體** 會有空格。

After:
   中文的\ **粗體**\ 有空格。

Noted that this has the same limitation as `Auto spacing`_. See
`Known exceptions and notices`_ for details.


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

``CJK_REMOVE_MARKUP_SPACING``
   Set to ``False`` to disable `Remove spacing around inline markups`_.
   Default to ``True``.
