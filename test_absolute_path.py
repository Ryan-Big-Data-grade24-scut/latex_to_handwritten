#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试绝对路径输出功能
"""

import os
import sys
from latex2handwritten import convert_latex

def test_absolute_path():
    """测试绝对路径输出功能"""
    print("测试绝对路径输出功能...")
    
    # 测试内容，确保会生成多页
    test_content = "第一页内容。\n\n第二页内容。\n\n第三页内容。\n\n第四页内容。\n\n第五页内容。"
    
    # 测试1：使用绝对路径输出
    print("\n测试1：使用绝对路径输出")
    output_path = r"e:\Ufolder\Current\ActionSys\TempProgram\latex_to_handwritten\test_absolute_output.png"
    
    try:
        # 确保目录存在
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成多页输出
        result = convert_latex(
            test_content,
            output_file=output_path,
            format="png",
            mixed_rendering=True,
            a4=True,
            max_score=2  # 每页只允许2行，确保生成多页
        )
        
        print(f"✓ 测试1成功！生成的文件：{result}")
        
        # 检查生成的文件
        files = result if isinstance(result, list) else [result]
        for file in files:
            if os.path.exists(file):
                print(f"  - 文件已存在：{file}")
                # 验证文件是否保存在指定的绝对路径下
                if os.path.dirname(file) == output_dir:
                    print(f"    ✅ 文件保存在正确的绝对路径目录")
                else:
                    print(f"    ❌ 文件保存在错误目录：{os.path.dirname(file)}")
            else:
                print(f"  ✗ 文件不存在：{file}")
        
        # 清理测试文件
        for file in files:
            if os.path.exists(file):
                os.remove(file)
                print(f"  - 已清理测试文件：{file}")
                
    except Exception as e:
        print(f"✗ 测试1失败：{e}")
        import traceback
        traceback.print_exc()
    
    print("\n测试完成！")

if __name__ == "__main__":
    test_absolute_path()