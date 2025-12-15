#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LaTeX公式标记处理脚本

功能：
1. 为文章中的$和$$前后添加空格
2. 智能处理：
   - $E=mc^2$ -> $ E=mc^2 $
   - $$E=mc^2$$ -> $$ E=mc^2 $$
   - 避免错误处理：$ $E=mc^2$ $ 或 $$$$E=mc^2$$$$
"""

import re
import os
import argparse

def process_latex_markers(text):
    """
    处理文本中的LaTeX公式标记，智能添加空格，同时处理列表项和标题
    
    Args:
        text (str): 原始文本
        
    Returns:
        str: 处理后的文本
    """
    if not text:
        return text
    
    # 1. 先处理双美元符号 $$...$$
    # 匹配 $$...$$ 模式，注意处理多行情况
    def replace_double_dollar(match):
        content = match.group(0)
        # 提取 $$ 之间的内容
        inner_content = content[2:-2].strip()
        # 重新构造带空格的形式
        return f'$$ {inner_content} $$'
    
    # 使用多行模式匹配 $$...$$
    text = re.sub(r'\$\$([\s\S]*?)\$\$', replace_double_dollar, text, flags=re.DOTALL)
    
    # 2. 再处理单美元符号 $...$
    # 匹配 $...$ 模式，注意排除已经处理过的 $$...$$ 中的 $ 符号
    def replace_single_dollar(match):
        content = match.group(0)
        # 提取 $ 之间的内容
        inner_content = content[1:-1].strip()
        # 重新构造带空格的形式
        return f'$ {inner_content} $'
    
    # 匹配单美元符号，排除已经处理过的 $$...$$ 中的 $ 符号
    pattern = r'(?<!\$)\$(?!\$)([\s\S]*?)(?<!\$)\$(?!\$)'
    text = re.sub(pattern, replace_single_dollar, text, flags=re.DOTALL)
    
    # 3. 确保 $ 和 $$ 前后与文本之间有空格
    # 处理单美元符号与文本之间的空格
    text = re.sub(r'([^\s\$])(\$)', r'\1 \2', text)
    text = re.sub(r'(\$)([^\s\$])', r'\1 \2', text)
    
    # 处理双美元符号与文本之间的空格
    text = re.sub(r'([^\s])(\$\$)', r'\1 \2', text)
    text = re.sub(r'(\$\$)([^\s])', r'\1 \2', text)
    
    # 4. 处理列表项，将 "- " 标记删除，确保每个列表项独立成行
    text = re.sub(r'^-\s+', '', text, flags=re.MULTILINE)
    
    # 5. 确保每一行都有显式的\n字符（即两个字符：反斜杠+n）
    # 首先将文本按实际换行符分割成原始行
    original_lines = text.splitlines()
    processed_parts = []
    
    for original_line in original_lines:
        line = original_line.strip()
        if line:
            # 非空行，确保行尾有显式的\n字符
            if line.startswith('#'):
                # 标题行，前后添加空行，每个标题独立成行，带显式\n
                processed_parts.append(line + ' \\n')
            else:
                # 普通行和列表项，每个独立成行，带显式\n
                processed_parts.append(line + ' \\n')
    
    # 合并所有处理后的部分
    processed_text = ''.join(processed_parts)
    
    # 6. 最后清理：移除首尾的多余空行
    processed_text = processed_text.strip()
    
    return processed_text

def process_file(input_file, output_file=None):
    """
    处理单个文件
    
    Args:
        input_file (str): 输入文件路径
        output_file (str, optional): 输出文件路径，默认为输入文件名加 _processed 后缀
    """
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 处理文本
    processed_content = process_latex_markers(content)
    
    # 确定输出文件路径
    if not output_file:
        base_name, ext = os.path.splitext(input_file)
        output_file = f"{base_name}_processed{ext}"
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(processed_content)
    
    print(f"处理完成：")
    print(f"输入文件：{input_file}")
    print(f"输出文件：{output_file}")
    print(f"文件大小：{len(content)} 字节 -> {len(processed_content)} 字节")

def process_directory(directory, recursive=False):
    """
    处理目录中的所有文本文件
    
    Args:
        directory (str): 目录路径
        recursive (bool): 是否递归处理子目录
    """
    supported_extensions = ['.txt', '.md', '.markdown', '.tex', '.latex']
    
    # 遍历目录
    if recursive:
        for root, dirs, files in os.walk(directory):
            for file in files:
                # 检查文件扩展名
                ext = os.path.splitext(file)[1].lower()
                if ext in supported_extensions:
                    file_path = os.path.join(root, file)
                    process_file(file_path)
    else:
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                ext = os.path.splitext(file)[1].lower()
                if ext in supported_extensions:
                    process_file(file_path)

def main():
    """
    主函数，处理命令行参数
    """
    parser = argparse.ArgumentParser(description='LaTeX公式标记处理脚本')
    parser.add_argument('-i', '--input', help='输入文件或目录路径')
    parser.add_argument('-o', '--output', help='输出文件路径（仅用于单个文件处理）')
    parser.add_argument('-r', '--recursive', action='store_true', help='递归处理目录中的文件')
    parser.add_argument('-t', '--test', action='store_true', help='运行测试用例')
    
    args = parser.parse_args()
    
    if args.test:
        # 运行测试用例
        test_cases = [
            # 单美元符号测试
            ("$E=mc^2$", "$ E=mc^2 $"),
            ("$ E=mc^2 $", "$ E=mc^2 $"),
            ("Text $E=mc^2$ text", "Text $ E=mc^2 $ text"),
            ("$ E=mc^2$text", "$ E=mc^2 $ text"),
            ("text$E=mc^2 $", "text $ E=mc^2 $"),
            
            # 双美元符号测试
            ("$$E=mc^2$$", "$$ E=mc^2 $$"),
            ("$$ E=mc^2 $$", "$$ E=mc^2 $$"),
            ("Text $$E=mc^2$$ text", "Text $$ E=mc^2 $$ text"),
            ("$$ E=mc^2$$text", "$$ E=mc^2 $$ text"),
            ("text$$E=mc^2 $$", "text $$ E=mc^2 $$"),
            
            # 混合测试
            ("$E=mc^2$ and $$F=ma$$", "$ E=mc^2 $ and $$ F=ma $$"),
            ("Text $E=mc^2$ and $$F=ma$$ text", "Text $ E=mc^2 $ and $$ F=ma $$ text"),
            
            # 多行测试
            ("$$\nE=mc^2\n$$", "$$ E=mc^2 $$"),
            ("$\nE=mc^2\n$", "$ E=mc^2 $"),
        ]
        
        print("运行测试用例...")
        passed = 0
        failed = 0
        
        for i, (input_text, expected) in enumerate(test_cases, 1):
            result = process_latex_markers(input_text)
            if result == expected:
                print(f"✓ 测试 {i} 通过")
                passed += 1
            else:
                print(f"✗ 测试 {i} 失败")
                print(f"  输入:  {repr(input_text)}")
                print(f"  期望: {repr(expected)}")
                print(f"  实际: {repr(result)}")
                failed += 1
        
        print(f"\n测试完成：{passed} 个通过，{failed} 个失败")
        return
    
    if not args.input:
        print("错误：必须指定输入文件或目录路径，或使用--test选项运行测试")
        parser.print_help()
        exit(1)
    
    if os.path.isfile(args.input):
        # 处理单个文件
        process_file(args.input, args.output)
    elif os.path.isdir(args.input):
        # 处理目录
        process_directory(args.input, args.recursive)
    else:
        print(f"错误：输入路径不存在：{args.input}")
        exit(1)

if __name__ == "__main__":
    main()