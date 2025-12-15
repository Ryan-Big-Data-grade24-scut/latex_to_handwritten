#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试自动换行功能
"""

from latex2handwritten import LatexToHandwritten

# 创建转换器实例
converter = LatexToHandwritten()

# 测试普通文本换行
print("=== 测试普通文本换行 ===")

# 测试用例1：长文本，不含公式
long_text = "这是一段非常长的普通文本，没有包含任何公式，用于测试自动换行功能是否正常工作。" * 3

# 转换前
print("原始文本：")
print(long_text)
print()

# 转换后
wrapped_text = converter._auto_wrap_text(long_text, max_chars=50)
print("换行后文本：")
print(wrapped_text)
print()

# 测试用例2：带显式换行符的文本
text_with_newlines = "这是第一段文本。\n这是第二段文本，包含更长的内容，需要自动换行。" * 2

print("=== 测试带显式换行符的文本 ===")
print("原始文本：")
print(text_with_newlines)
print()

wrapped_text2 = converter._auto_wrap_text(text_with_newlines, max_chars=50)
print("换行后文本：")
print(wrapped_text2)
print()

# 测试用例3：包含公式的文本
text_with_formulas = "这是一段包含公式的文本，$E=mc^2$ 是著名的质能方程，而 $F=ma$ 是牛顿第二定律。" * 2

print("=== 测试包含公式的文本 ===")
print("原始文本：")
print(text_with_formulas)
print()

wrapped_text3 = converter._auto_wrap_text(text_with_formulas, max_chars=50)
print("换行后文本：")
print(wrapped_text3)
