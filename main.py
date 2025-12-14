import click
from latex2handwritten import convert_latex, get_available_fonts
import os

@click.command()
@click.argument('latex')
@click.option('--output', '-o', default='output.png', help='输出文件路径')
@click.option('--font', '-f', default='Comic Neue', help='手写字体名称')
@click.option('--resolution', '-r', default=200, help='图片分辨率（DPI）')
@click.option('--width', '-w', default=800, help='图片宽度（像素）')
@click.option('--height', '-h', default=200, help='图片高度（像素）')
@click.option('--randomness', '-R', default=0.05, help='随机效果强度（0-1）')
@click.option('--bg-color', '-b', default='white', help='背景颜色')
@click.option('--text-color', '-t', default='black', help='文字颜色')
@click.option('--format', '-F', default='png', type=click.Choice(['png', 'jpg', 'svg']), help='输出格式')
@click.option('--list-fonts', '-l', is_flag=True, help='列出可用的手写字体')
def main(latex, output, font, resolution, width, height, randomness, bg_color, text_color, format, list_fonts):
    """
    将LaTeX公式转换为手写风格图片
    
    LATEX: LaTeX公式字符串，例如：$E=mc^2$
    """
    # 如果请求列出字体
    if list_fonts:
        fonts = get_available_fonts()
        click.echo("可用的手写字体：")
        for f in fonts:
            click.echo(f"  - {f}")
        return
    
    # 验证随机效果强度
    if not 0 <= randomness <= 1:
        click.echo("错误：随机效果强度必须在0到1之间")
        return
    
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
            format=format
        )
        
        click.echo(f"成功生成手写公式图片：{output_file}")
    except Exception as e:
        click.echo(f"错误：{e}")

if __name__ == '__main__':
    main()
