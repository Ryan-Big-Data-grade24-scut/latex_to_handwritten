from latex2handwritten import LatexToHandwritten

# 测试公式识别
converter = LatexToHandwritten()

test_text = "The magnitude of the current density vector is $J = \frac{i}{A} = \frac{i}{\pi d^2/4} = \frac{4(1.2 \times 10^{-10} A)}{\pi(2.5 \times 10^{-3} m)^2} = 2.4 \times 10^{-5} A/m^2$."

print("原始文本:")
print(test_text)
print("\n公式识别结果:")
parts = converter._split_text_formulas(test_text)
for i, (part_type, content) in enumerate(parts):
    print(f"{i+1}. 类型: {part_type}, 内容: {content}")

# 测试块级公式
block_test = "The current resulting from this non-uniform current density is $$i = \int_{cylinder } J_{a} dA = \frac{J_0}{R} \int_{0}^{R} r \cdot 2\pi r dr = \frac{2}{3}\pi R^2 J_0 = \frac{2}{3}\pi(3.40 \times 10^{-3} m)^2(5.50 \times 10^4 A/m^2) = 1.33 A.$$"

print("\n\n块级公式识别结果:")
block_parts = converter._split_text_formulas(block_test)
for i, (part_type, content) in enumerate(block_parts):
    print(f"{i+1}. 类型: {part_type}, 内容: {content}")
