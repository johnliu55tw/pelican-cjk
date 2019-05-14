Pelican in CJK
##############

Writting Chinese, Japanese and Korean in Pelican smoothly.

NOTE:
   This plugin currently only works when writting in **reStructuredText**.
   It might not work correctly for Markdown. See `Behavior Changes`_ for details.

Behavior Changes
****************

1. Auto spacing
===============

Insert spaces between an half-width (Alphabets, Numbers, Symbols) word
surrounded by CJK charaters.

Before:
   中間的English Vocabulary很Beautiful。

After:
   中間的 English Vocabulary 單字很 Beautiful。

Noted that if the neighbor CJK character is a **punctuation**, space will not be
added.

2. Remove newline for Chinese paragraph
=======================================

Newline characters in a paragraph will be kept in the output HTML. Browser will
then interpret this newline character as a **space**. This is fine in English,
but it looks weird in CJK. This plugin solve this problem by removed a newline
character surrounded by CJK characters.

Before:
   這是第一行
   和第二行

After:
   這是第一行和第二行
