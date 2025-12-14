import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont
import random

# 设置中文字体为黑体，解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 配置matplotlib使用LaTeX并设置字体
plt.rcParams['text.usetex'] = False
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'sans'
plt.rcParams['mathtext.it'] = 'sans:italic'
plt.rcParams['mathtext.bf'] = 'sans:bold'

class LatexToHandwritten:
    def __init__(self):
        self.fonts_dir = os.path.join(os.path.dirname(__file__), 'fonts')
        self.available_fonts = self._load_available_fonts()
    
    def _load_available_fonts(self):
        """加载可用的手写字体"""
        available_fonts = {}
        
        # 检查系统中是否已安装常见的手写字体
        system_fonts = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
        
        # 常见的手写风格字体
        handwritten_fonts = [
            'Comic Neue',
            'Comic Sans MS',
            'Humor Sans',
            'Handlee',
            'Architects Daughter',
            'Indie Flower',
            'Caveat',
            'Dancing Script'
        ]
        
        for font_name in handwritten_fonts:
            for font_path in system_fonts:
                if font_name.lower() in font_path.lower():
                    available_fonts[font_name] = font_path
                    break
        
        # 加载项目目录中的字体
        if os.path.exists(self.fonts_dir):
            for font_file in os.listdir(self.fonts_dir):
                if font_file.endswith('.ttf') or font_file.endswith('.otf'):
                    font_name = os.path.splitext(font_file)[0]
                    available_fonts[font_name] = os.path.join(self.fonts_dir, font_file)
        
        # 如果没有找到手写字体，使用默认字体
        if not available_fonts:
            available_fonts['Default'] = None
        
        return available_fonts
    
    def convert_latex(self, latex, output_file="output.png", font="IndieFlower-Regular", 
                     resolution=200, width=800, height=200, randomness=0.05,
                     bg_color="white", text_color="black", format="png", a4=False):
        """
        将LaTeX公式转换为手写风格图片
        
        参数:
            latex: str - LaTeX公式字符串，支持多行
            output_file: str - 输出文件路径
            font: str - 手写字体名称
            resolution: int - 图片分辨率（DPI）
            width: int - 图片宽度（像素），当a4为True时忽略
            height: int - 图片高度（像素），当a4为True时忽略
            randomness: float - 随机效果强度（0-1）
            bg_color: str - 背景颜色
            text_color: str - 文字颜色
            format: str - 输出格式（png/jpg/svg）
            a4: bool - 是否使用A4格式（210mm × 297mm）
        """
        # 选择字体
        font_path = self.available_fonts.get(font, None)
        
        # 如果找到了字体文件，配置matplotlib使用该字体
        if font_path:
            # 添加字体到matplotlib字体管理器
            font_manager.fontManager.addfont(font_path)
            
            # 获取字体名称
            font_name = font_manager.FontProperties(fname=font_path).get_name()
            
            # 设置matplotlib使用该字体
            plt.rcParams['font.family'] = ['sans-serif']
            plt.rcParams['font.sans-serif'] = [font_name, 'SimHei']
            
            # 设置数学公式也使用该字体
            plt.rcParams['mathtext.fontset'] = 'custom'
            plt.rcParams['mathtext.rm'] = font_name
            plt.rcParams['mathtext.it'] = f'{font_name}:italic'
            plt.rcParams['mathtext.bf'] = f'{font_name}:bold'
        
        # 计算A4尺寸（mm转英寸，1英寸=25.4mm）
        if a4:
            a4_width = 210 / 25.4  # 英寸
            a4_height = 297 / 25.4  # 英寸
            figsize = (a4_width, a4_height)
        else:
            # 像素转英寸（1英寸=100像素默认，根据resolution调整）
            figsize = (width / resolution, height / resolution)
        
        # 创建一个临时图来渲染LaTeX
        fig, ax = plt.subplots(figsize=figsize, dpi=resolution)
        
        # 设置背景颜色
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        
        # 渲染LaTeX公式（支持多行）
        # 将\n替换为换行符，支持多行输入
        latex = latex.replace('\\n', '\n')
        ax.text(0.5, 0.5, latex, fontsize=48, ha='center', va='center',
                color=text_color, transform=ax.transAxes, linespacing=1.5)
        
        # 隐藏坐标轴
        ax.axis('off')
        
        # 调整布局
        plt.tight_layout(pad=0)
        
        # 保存临时图片
        temp_file = "temp_latex.png"
        plt.savefig(temp_file, dpi=resolution, format='png', bbox_inches='tight', pad_inches=0, transparent=(bg_color == 'transparent'))
        plt.close()
        
        # 读取临时图片
        img = Image.open(temp_file)
        
        # 添加手写效果
        if randomness > 0:
            img = self._add_handwriting_effect(img, randomness, text_color)
        
        # 保存最终图片
        img.save(output_file, format=format)
        
        # 清理临时文件
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        return output_file
    
    def _add_handwriting_effect(self, img, randomness, text_color):
        """添加手写效果：轻微的位置偏移和旋转"""
        width, height = img.size
        
        # 创建新图片
        new_img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        
        # 转换为RGBA模式
        img = img.convert('RGBA')
        
        # 对每个像素应用轻微的随机偏移
        pixels = img.load()
        new_pixels = new_img.load()
        
        for x in range(width):
            for y in range(height):
                r, g, b, a = pixels[x, y]
                if a > 128:  # 只处理不透明的像素
                    # 应用随机偏移
                    offset_x = int(random.uniform(-randomness*10, randomness*10))
                    offset_y = int(random.uniform(-randomness*10, randomness*10))
                    
                    new_x = x + offset_x
                    new_y = y + offset_y
                    
                    if 0 <= new_x < width and 0 <= new_y < height:
                        new_pixels[new_x, new_y] = (r, g, b, a)
        
        return new_img
    
    def _apply_handwritten_font(self, img, latex, font_path, text_color, bg_color):
        """尝试使用指定的手写字体重新渲染公式"""
        # 注意：直接使用PIL渲染复杂LaTeX公式比较困难
        # 这里我们使用一种简化的方法，仅作为演示
        # 对于复杂公式，建议使用默认的matplotlib渲染
        
        # 创建新图片
        width, height = img.size
        new_img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(new_img)
        
        try:
            # 加载字体
            font_size = 48
            pil_font = ImageFont.truetype(font_path, font_size)
            
            # 简单文本渲染（仅适用于基本公式）
            # 注意：这不会处理复杂的LaTeX命令
            text = latex.replace('$', '')
            draw.text((width/2, height/2), text, fill=text_color, font=pil_font, 
                     anchor='mm')
            
            return new_img
        except Exception as e:
            # 如果渲染失败，返回原始图片
            print(f"Error applying handwritten font: {e}")
            return img.convert('RGB')

# 创建全局实例
_converter = LatexToHandwritten()

# 导出便捷函数
def convert_latex(latex, output_file="output.png", font="IndieFlower-Regular", 
                 resolution=200, width=800, height=200, randomness=0.05,
                 bg_color="white", text_color="black", format="png", a4=False):
    """便捷函数：将LaTeX公式转换为手写风格图片"""
    return _converter.convert_latex(latex, output_file, font, resolution, 
                                  width, height, randomness, bg_color, 
                                  text_color, format, a4)

def get_available_fonts():
    """获取可用的手写字体列表"""
    return list(_converter.available_fonts.keys())
