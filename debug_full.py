import os

# 直接读取文件，不使用click库
file_path = "examples/26-28.txt"

print(f"读取文件: {file_path}")
print("=" * 60)

# 1. 直接读取文件，检查原始内容
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("1. 文件原始内容 (前500字符):")
print(repr(content[:500]))
print("\n2. 文件原始内容中\frac的表示:")
# 查找\frac
frac_pos = content.find('\\frac')
if frac_pos != -1:
    print(f"找到\\frac在位置 {frac_pos}")
    # 打印上下文
    start = max(0, frac_pos - 5)
    end = min(len(content), frac_pos + 15)
    print(f"上下文: {repr(content[start:end])}")
    # 检查每个字符的十六进制表示
    print("