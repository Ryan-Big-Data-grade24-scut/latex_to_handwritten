#!/usr/bin/env python3
"""
LaTeX 标记处理模块

用于处理和转换特殊的 LaTeX 标记，确保它们能被正确渲染
"""

import re

def process_latex_markers(content):
    """
    处理和转换特殊的 LaTeX 标记
    
    参数:
        content: str - 包含 LaTeX 标记的内容
    
    返回:
        str - 处理后的内容
    """
    # 替换常见的 LaTeX 环境标记
    content = re.sub(r'\\begin\{equation\}(.*?)\\end\{equation\}', r'$$\1$$', content, flags=re.DOTALL)
    content = re.sub(r'\\begin\{align\}(.*?)\\end\{align\}', r'$$\1$$', content, flags=re.DOTALL)
    content = re.sub(r'\\begin\{gather\}(.*?)\\end\{gather\}', r'$$\1$$', content, flags=re.DOTALL)
    
    # 替换常见的 LaTeX 命令
    content = re.sub(r'\\\[([^\]]+)\\\]', r'$$\1$$', content, flags=re.DOTALL)
    content = re.sub(r'\\\(([^\)]+)\\\)', r'$\1$', content, flags=re.DOTALL)
    
    # 替换特殊字符
    content = re.sub(r'\\alpha', r'\alpha', content)
    content = re.sub(r'\\beta', r'\beta', content)
    content = re.sub(r'\\gamma', r'\gamma', content)
    content = re.sub(r'\\delta', r'\delta', content)
    content = re.sub(r'\\epsilon', r'\epsilon', content)
    
    # 替换换行符
    content = re.sub(r'\\\\', r'\n', content)
    
    return content

if __name__ == "__main__":
    # 测试函数
    test_content = """
\begin{equation}
E = mc^2
\end{equation}

\[F = ma\]

Some inline formula: \\(a^2 + b^2 = c^2\\)
    """
    
    print("原始内容:")
    print(test_content)
    print("\n处理后:")
    print(process_latex_markers(test_content))