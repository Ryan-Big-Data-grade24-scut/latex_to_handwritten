#!/usr/bin/env python3
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from latex2handwritten import _converter

# 打印加载的字体数量
print(f"加载的字体数量: {len(_converter.all_ttf_fonts)}")

# 打印前10个字体文件路径
print("\n前10个字体文件:")
for font_path in _converter.all_ttf_fonts[:10]:
    print(font_path)

# 测试随机选择
if _converter.all_ttf_fonts:
    import random
    random_font = random.choice(_converter.all_ttf_fonts)
    print(f"\n随机选择的字体: {random_font}")
else:
    print("\n没有加载到任何字体文件!")

# 检查fonts目录
fonts_dir = _converter.fonts_dir
print(f"\nFonts目录: {fonts_dir}")
print(f"目录存在: {os.path.exists(fonts_dir)}")

# 直接列出目录内容
if os.path.exists(fonts_dir):
    print("\n目录内容:")
    for root, dirs, files in os.walk(fonts_dir):
        level = root.replace(fonts_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if file.endswith('.ttf'):
                print(f"{subindent}{file}")