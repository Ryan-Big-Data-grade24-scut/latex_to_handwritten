from latex2handwritten import LatexToHandwritten

# 测试公式识别
converter = LatexToHandwritten()

test_text = "The magnitude of the current density vector is $J = \frac{i}{A} = \frac{i}{\pi d^2/4} = \frac{4(1.2 \times 10^{-10} A)}{\pi(2.5 \times 10^{-3} m)^2} = 2.4 \times 10^{-5} A/m^2$."

print("原始文本:")
print(test_text)
print("\n公式识别结果:")
parts = converter._split_text_formulas(test_text)
for i, (part_type, content