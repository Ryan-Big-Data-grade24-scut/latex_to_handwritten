#!/usr/bin/env python3
"""
测试 LaTeX 标记处理函数
"""

from process_latex_markers import process_latex_markers

# 测试用例
test_cases = [
    "Hello World",
    "$E = mc^2$",
    "\[F = ma\]",
    "\\(a^2 + b^2 = c^2\\)",
    "\begin{equation}E = mc^2\end{equation}"
]

print("=== 测试 LaTeX 标记处理函数 ===")
for i, test in enumerate(test_cases):
    print(f"\n测试用例 {i+1}: {repr(test)}")
    try:
        result = process_latex_markers(test)
        print(f"✓ 成功: {repr(result)}")
    except Exception as e:
        print(f"✗ 失败: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

print("\n=== 测试完成 ===")
