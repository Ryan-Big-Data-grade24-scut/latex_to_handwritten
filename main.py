import click
from latex2handwritten import convert_latex, get_available_fonts
import os

@click.command()
@click.argument('latex', required=False, default='')
@click.option('--output', '-o', default='output.png', help='输出文件路径')
@click.option('--font', '-f', default='IndieFlower-Regular', help='手写字体名称')
@click.option('--resolution', '-r', default=200, help='图片分辨率（DPI）')
@click.option('--width', '-w', default=800, help='图片宽度（像素），当使用A4格式时忽略')
@click.option('--height', '-h', default=200, help='图片高度（像素），当使用A4格式时忽略')
@click.option('--randomness', '-R', default=0.05, help='随机效果强度（0-1）')
@click.option('--bg-color', '-b', default='white', help='背景颜色')
@click.option('--text-color', '-t', default='black', help='文字颜色')
@click.option('--format', '-F', default='png', type=click.Choice(['png', 'jpg', 'svg']), help='输出格式')
@click.option('--list-fonts', '-l', is_flag=True, help='列出可用的手写字体')
@click.option('--a4', is_flag=True, help='使用A4格式（210mm × 297mm）')
@click.option('--input-file', '-i', type=click.File('r', encoding='utf-8'), help='从文件读取多行LaTeX内容')
@click.option('--markdown', '-m', is_flag=True, help='将内容作为markdown处理')
@click.option('--random-fonts', '-rf', is_flag=True, help='每个字符随机使用不同字体')
@click.option('--mixed-rendering', '-mr', is_flag=True, help='使用混合渲染（正文随机字体，公式传统渲染）')
def main(latex, output, font, resolution, width, height, randomness, bg_color, text_color, format, list_fonts, a4, input_file, markdown, random_fonts, mixed_rendering):
    """
    将LaTeX公式转换为手写风格图片
    
    LATEX: LaTeX公式字符串，例如：$E=mc^2$，支持使用\\n分隔多行
    
    示例：
    单公式：python main.py "$E=mc^2$"
    多行公式：python main.py "$E=mc^2$\\n$F=ma$"
    从文件读取：python main.py -i formulas.txt --a4
    随机字体：python main.py "Hello World" --random-fonts
    Markdown：python main.py -i document.md --markdown --a4
    """
    # 如果请求列出字体
    if list_fonts:
        fonts = get_available_fonts()
        click.echo("可用的手写字体：")
        for f in fonts:
            click.echo(f"  - {f}")
        return
    
    # 从文件读取LaTeX内容
    if input_file:
        latex = input_file.read()
    
    # 验证随机效果强度
    if not 0 <= randomness <= 1:
        click.echo("错误：随机效果强度必须在0到1之间")
        return
    
    # 检查是否有LaTeX内容
    if not latex.strip():
        click.echo("错误：没有提供LaTeX内容，请使用参数或文件输入")
        return
    
    # 只有当output是简单文件名（不是绝对路径，也不是包含目录的路径）时，才默认保存到examples目录
    # 对于绝对路径或包含目录的路径，直接使用用户指定的路径
    if not os.path.isabs(output) and '\\' not in output and '/' not in output and ':' not in output:
        # 保持向后兼容，默认保存到examples目录
        output = os.path.join("examples", output)
    
    try:
        # 调用转换函数
        output_file = convert_latex(
            latex=latex,
            output_file=output,
            font=font,
            resolution=resolution,
            width=width,
            height=height,
            randomness=randomness,
            bg_color=bg_color,
            text_color=text_color,
            format=format,
            a4=a4,
            markdown=markdown,
            random_fonts=random_fonts,
            mixed_rendering=mixed_rendering
        )
        
        click.echo(f"成功生成手写公式图片：{output_file}")
    except Exception as e:
        click.echo(f"错误：{e}")

if __name__ == '__main__':
    main()
