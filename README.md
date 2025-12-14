# LaTeX to Handwritten Image Generator

一个将LaTeX数学公式转换为手写风格图片的Python工具包。

## 项目状态

✅ **已完成核心功能开发**
✅ **已通过测试用例验证**
✅ **支持命令行和API两种使用方式**
✅ **可生成多种手写风格效果**

## 功能特性

- 支持将复杂的LaTeX数学公式转换为手写风格图片
- 提供多种手写字体选择（自动检测系统字体）
- 可自定义图片尺寸、分辨率和背景
- 支持多种输出格式（PNG、JPG、SVG）
- 提供命令行和API两种使用方式
- 支持随机手写效果（位置偏移、旋转等）
- 支持中文显示（已配置中文字体）

## 安装

### 使用conda虚拟环境（推荐）

```bash
# 创建虚拟环境
conda create -n latex_handwritten python=3.10 -y

# 激活虚拟环境
conda activate latex_handwritten

# 安装依赖
pip install -r requirements.txt
```

### 使用pip安装依赖

```bash
# 克隆项目
git clone <repository-url>
cd latex_to_handwritten

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 命令行使用

```bash
# 基本使用
python main.py "$E=mc^2$" --output einstein.png

# 自定义参数
python main.py "$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$" --output integral.png --resolution 300 --randomness 0.1

# 列出可用字体
python main.py --list-fonts
```

### API使用

```python
from latex2handwritten import convert_latex

# 基本使用
convert_latex(r"$E=mc^2$", output_file="einstein.png")

# 自定义参数
convert_latex(
    r"$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$",
    output_file="integral.png",
    resolution=300,
    randomness=0.1,
    bg_color="white"
)
```

## 参数说明

| 参数 | 类型 | 描述 | 默认值 |
|------|------|------|--------|
| latex | str | LaTeX公式字符串 | 必填 |
| output_file | str | 输出文件路径 | output.png |
| font | str | 手写字体名称 | Comic Neue |
| resolution | int | 图片分辨率（DPI） | 200 |
| width | int | 图片宽度（像素） | 800 |
| height | int | 图片高度（像素） | 200 |
| randomness | float | 随机效果强度（0-1） | 0.05 |
| bg_color | str | 背景颜色 | white |
| text_color | str | 文字颜色 | black |
| format | str | 输出格式（png/jpg/svg） | png |

## 支持的公式类型

- 基本算术运算
- 代数表达式
- 微积分（积分、导数）
- 三角函数和对数函数
- 极限和求和
- 简单矩阵（目前不支持复杂矩阵）

## 实际示例

### 已生成的示例图片

项目已成功生成以下示例图片：

- **einstein.png** - 爱因斯坦质能方程
- **quadratic.png** - 二次方程求根公式
- **gaussian_integral.png** - 高斯积分
- **trigonometry.png** - 三角恒等式
- **limit.png** - 极限示例
- **derivative.png** - 幂函数导数

### 不同随机效果对比

- **einstein_random_0.0.png** - 无随机效果
- **einstein_random_0.1.png** - 轻微随机效果
- **einstein_random_0.2.png** - 较强随机效果

## 命令行示例

```bash
# 生成爱因斯坦方程图片
python main.py "$E=mc^2$" --output cmd_test.png --randomness 0.1
# 输出: 成功生成手写公式图片：cmd_test.png
```

## 已知限制

- 复杂矩阵支持有限（当前版本对复杂矩阵渲染可能失败）
- 手写字体依赖系统安装或手动添加到fonts目录
- SVG格式输出可能不支持某些高级效果

## 字体说明

### 系统字体检测

项目会自动检测系统中已安装的手写字体，包括：
- Comic Neue
- Comic Sans MS
- Humor Sans
- Handlee
- Architects Daughter
- Indie Flower
- Caveat
- Dancing Script

### 添加自定义字体

您可以将手写字体文件（.ttf或.otf格式）添加到`fonts/`目录中，系统会自动识别并使用。

## 测试

### 运行测试脚本

```bash
# 测试字体检测
python test_fonts.py

# 运行完整测试套件
python test_conversion.py
```

### 测试结果

项目已通过7个测试用例，包括：
- 简单公式（E=mc²）
- 二次方程求根公式
- 高斯积分
- 三角恒等式
- 极限示例
- 幂函数导数

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

### 贡献指南

1. Fork本项目
2. 创建功能分支（`git checkout -b feature/AmazingFeature`）
3. 提交更改（`git commit -m 'Add some AmazingFeature'`）
4. 推送到分支（`git push origin feature/AmazingFeature`）
5. 打开Pull Request

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交Issue
- 发送邮件

## 致谢

感谢所有为项目做出贡献的开发者和用户！
