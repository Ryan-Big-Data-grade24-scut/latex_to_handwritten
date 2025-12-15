import re

# 测试正则表达式
formula_pattern = r'(\$\$.*?\$\$)|(\$[^$\n]*\$)|(\\\[.*?\\\])'

test_text = "$J = \frac{i}{A}$"

print("原始文本:", repr(test_text))

matches = list(re.finditer(formula_pattern, test_text, re.DOTALL))
for match in matches:
    print("匹配到:", repr(match.group()))
    print("组:", [repr(g) for g in match.groups()])

# 测试多行
multiline = "$$i = \int_{cylinder } J_{a} dA = \frac{J_0}{R} \int_{0}^{R} r \cdot 2\pi r dr$$"
print("\n多行测试:")
print("原始文本:", repr(multiline))

matches = list(re.finditer(formula_pattern, multiline, re.DOTALL))
for match in matches:
    print("匹配到:", repr(match.group()))
