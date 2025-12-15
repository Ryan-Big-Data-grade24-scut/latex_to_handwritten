#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LaTeX 公式渲染调试工具

功能：
1. 测试公式分割功能
2. 测试分页功能
3. 测试渲染功能
4. 提供详细的调试信息
"""

import argparse
import os
import sys
from latex2handwritten import convert_latex, LatexToHandwritten


def debug_formula(formula, output_file="debug_result.png"):
    """
    调试LaTeX公式渲染
    
    参数:
        formula: str - 要调试的公式
        output_file: str - 输出文件名
    """
    print("=== LaTeX 公式渲染调试工具 ===")
    print(f"公式内容: {formula}")
    print(f"输出文件: {output_file}")
    print()
    
    try:
        # 初始化转换器
        converter = LatexToHandwritten()
        print("✓ 初始化转换器成功")
        print()
        
        # 1. 测试公式分割
        print("1. 测试公式分割:")
        content_items = converter._split_text_formulas(formula)
        print(f"   分割结果: {content_items}")
        print()
        
        # 2. 测试分页
        print("2. 测试分页:")
        pages = converter._paginate_content(content_items)
        print(f"   分页结果: {len(pages)} 页")
        print()
        
        # 3. 测试渲染
        print("3. 测试渲染:")
        
        # 使用convert_latex函数进行完整渲染测试
        output_files = convert_latex(
            latex=formula,
            output_file=output_file,
            font="IndieFlower-Regular",
            resolution=200,
            randomness=0.05,
            a4=False,
            markdown=False,
            random_fonts=False,
            mixed_rendering=False,
            format="png"
        )
        
        print(f"✓ 渲染成功: {output_files}")
        print(f"   渲染结果已保存到: {os.path.abspath(output_files)}")
        print()
        
        # 4. 测试混合渲染
        print("4. 测试混合渲染:")
        mixed_output = output_file.replace('.png', '_mixed.png')
        output_files_mixed = convert_latex(
            latex=formula,
            output_file=mixed_output,
            font="IndieFlower-Regular",
            resolution=200,
            randomness=0.05,
            a4=False,
            markdown=False,
            random_fonts=True,
            mixed_rendering=True,
            format="png"
        )
        print(f"✓ 混合渲染成功: {output_files_mixed}")
        print(f"   混合渲染结果已保存到: {os.path.abspath(output_files_mixed)}")
        
    except Exception as e:
        print(f"✗ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=== 调试完成 ===")
    print()
    print("建议:")
    print("1. 检查公式语法是否正确")
    print("2. 确保已安装所有依赖库")
    print("3. 尝试调整渲染参数")
    print("4. 查看生成的图片，检查渲染效果")


def test_common_formulas():
    """
    测试多种常见公式
    """
    common_formulas = [
        "$E = mc^2$",
        "$F = ma$",
        "$a^2 + b^2 = c^2$",
        "$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$",
        "$\int_{a}^{b} f(x) dx$",
        "$\lim_{x \to \infty} \frac{1}{x} = 0$",
        "$e^{i\pi} + 1 = 0$",
        "$\nabla \cdot \vec{E} = \frac{\rho}{\epsilon_0}$",
        "$\frac{\partial u}{\partial t} = \alpha \nabla^2 u$"
    ]
    
    print("=== 测试多种常见公式 ===")
    print(f"共测试 {len(common_formulas)} 种公式")
    print()
    
    for i, formula in enumerate(common_formulas, 1):
        print(f"测试公式 {i}: {formula}")
        output_file = f"test_formula_{i}.png"
        try:
            convert_latex(
                latex=formula,
                output_file=output_file,
                font="IndieFlower-Regular",
                resolution=200,
                randomness=0.05,
                a4=False,
                markdown=False,
                random_fonts=False,
                mixed_rendering=False,
                format="png"
            )
            print(f"   ✓ 成功")
        except Exception as e:
            print(f"   ✗ 失败: {str(e)}")
    
    print()
    print("=== 公式测试完成 ===")
    print("请查看生成的test_formula_*.png文件")


def list_available_fonts():
    """
    列出可用的手写字体
    """
    print("=== 可用的手写字体 ===")
    converter = LatexToHandwritten()
    available_fonts = converter.available_fonts
    
    if available_fonts:
        for font_name, font_path in available_fonts.items():
            print(f"- {font_name}: {font_path}")
    else:
        print("没有找到可用的手写字体")
    
    print()


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description="LaTeX 公式渲染调试工具")
    parser.add_argument("formula", nargs="?", help="要调试的公式")
    parser.add_argument("-o", "--output", default="debug_result.png", help="输出文件名")
    parser.add_argument("-l", "--list-fonts", action="store_true", help="列出可用字体")
    parser.add_argument("-t", "--test", action="store_true", help="测试多种常见公式")
    
    args = parser.parse_args()
    
    if args.list_fonts:
        list_available_fonts()
    elif args.test:
        test_common_formulas()
    elif args.formula:
        debug_formula(args.formula, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()