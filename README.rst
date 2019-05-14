Pelican in CJK
##############

Writting Chinese, Japanese and Korean in Pelican smoothly.

NOTE:
   This plugin currently only works when writting in **reStructuredText**.
   It might not work correctly for Markdown. See `Behavior Changes`_ for details.

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

Noted that if the neighbor CJK character is a **punctuation**, space will not be
added.

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
