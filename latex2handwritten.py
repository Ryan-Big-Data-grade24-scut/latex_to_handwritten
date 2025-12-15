import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont
import random
import re
from markdown import markdown
from io import BytesIO

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
        self.all_ttf_fonts = self._load_all_ttf_fonts()
    
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
    
    def _load_all_ttf_fonts(self):
        """加载所有.ttf字体，包括子目录"""
        all_fonts = []
        
        # 遍历所有目录和子目录
        for root, dirs, files in os.walk(self.fonts_dir):
            for file in files:
                if file.endswith('.ttf'):
                    font_path = os.path.join(root, file)
                    all_fonts.append(font_path)
        
        return all_fonts
    
    def convert_latex(self, latex, output_file="output.png", font="IndieFlower-Regular", 
                     resolution=200, width=800, height=200, randomness=0.05,
                     bg_color="white", text_color="black", format="png", a4=False,
                     markdown=False, random_fonts=False, mixed_rendering=False, max_chars=50, max_score=15):
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
            markdown: bool - 是否将内容作为markdown处理
            random_fonts: bool - 是否每个字符随机使用不同字体
            mixed_rendering: bool - 是否使用混合渲染（正文随机字体，公式传统渲染）
            max_chars: int - 每行最大字符数
            max_score: int - 每页最大分数（普通行1分，公式行2分）
        """
        # 如果是markdown，先转换为纯文本
        if markdown:
            # 将markdown转换为纯文本（移除markdown语法）
            text_content = re.sub(r'#+\s*', '', latex)  # 移除标题
            text_content = re.sub(r'\*\*(.*?)\*\*', r'\1', text_content)  # 移除粗体
            text_content = re.sub(r'\*(.*?)\*', r'\1', text_content)  # 移除斜体
            text_content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text_content)  # 移除链接
            text_content = re.sub(r'\n{3,}', '\n\n', text_content)  # 合并空行
            latex = text_content
        
        # 计算A4尺寸（mm转英寸，1英寸=25.4mm）
        # A4竖版：210mm × 297mm（宽×高）
        if a4:
            a4_width = 210 / 25.4  # 英寸
            a4_height = 297 / 25.4  # 英寸
            figsize = (a4_width, a4_height)
        else:
            # 像素转英寸（1英寸=100像素默认，根据resolution调整）
            figsize = (width / resolution, height / resolution)
        
        # 分割文本和公式
        content_items = self._split_text_formulas(latex)
        
        # 分页处理
        pages = self._paginate_content(content_items, max_score)
        
        # 渲染每一页
        output_files = []
        for i, page_items in enumerate(pages):
            # 渲染单页内容
            img = self._render_page(page_items, figsize, resolution, bg_color, text_color, randomness, mixed_rendering, random_fonts)
            
            # 生成输出文件名
            if len(pages) > 1:
                # 多页输出，添加页码
                base_name, ext = os.path.splitext(output_file)
                page_output_file = f"{base_name}_page_{i+1}{ext}"
            else:
                # 单页输出
                page_output_file = output_file
            
            # 保存最终图片
            img.save(page_output_file, format=format)
            output_files.append(page_output_file)
        
        return output_files if len(output_files) > 1 else output_files[0]
    
    def _render_with_random_fonts(self, text, resolution, a4, figsize, bg_color, text_color, randomness):
        """
        使用随机字体逐个字符渲染文本
        """
        # 转换英寸为像素
        width_px = int(figsize[0] * resolution)
        height_px = int(figsize[1] * resolution)
        
        # 创建空白图片
        img = Image.new('RGB', (width_px, height_px), bg_color)
        draw = ImageDraw.Draw(img)
        
        # 计算文本区域
        margin = int(width_px * 0.1)  # 10%边距
        text_area_width = width_px - 2 * margin
        
        # 解析文本为行
        lines = text.split('\n')
        
        # 基本字体大小
        base_font_size = 48
        
        # 初始位置
        x = margin
        y = margin + base_font_size
        
        # 加载所有可用字体
        available_fonts = self.all_ttf_fonts
        
        # 处理每一行
        for line in lines:
            if not line.strip():
                y += base_font_size * 1.5
                continue
            
            # 处理行中的每个字符
            for char in line:
                if char.isspace():
                    # 空格处理
                    x += base_font_size * 0.4
                    continue
                
                try:
                    # 直接绘制字符，不使用临时图片和旋转
                    # 随机选择字体
                    random_font_path = random.choice(available_fonts)
                    
                    # 随机调整字体大小（±20%）
                    random_size = int(base_font_size * (0.8 + random.random() * 0.4))
                    
                    # 加载字体
                    pil_font = ImageFont.truetype(random_font_path, random_size)
                    
                    # 随机位置偏移
                    offset_x = int(random.uniform(-randomness*8, randomness*8))
                    offset_y = int(random.uniform(-randomness*8, randomness*8))
                    
                    # 直接绘制字符到主图片
                    draw.text((x + offset_x, y + offset_y), char, font=pil_font, fill=text_color)
                    
                    # 使用固定宽度估计，避免bbox问题
                    char_width = random_size * 0.6
                    
                    # 更新x坐标
                    x += char_width
                    
                    # 换行检查
                    if x > width_px - margin:
                        x = margin
                        y += base_font_size * 1.5
                        break
                    
                except Exception as e:
                    # 如果字体加载失败，使用默认字体大小
                    draw.text((x, y), char, font=ImageFont.load_default(), fill=text_color)
                    x += base_font_size * 0.5
            
            # 换行
            x = margin
            y += base_font_size * 1.5
            
            # 检查是否超出页面高度
            if y > height_px - margin:
                break
        
        return img
    
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
    
    def _split_text_formulas(self, content):
        """
        将内容分割为正文和公式部分
        
        参数:
            content: str - 包含文本和公式的内容
        
        返回:
            list - 包含文本和公式的列表，每个元素是一个字典，包含type和content字段
        """
        # 定义公式正则表达式
        patterns = [
            # 块级公式 $$...$$
            (r'\$\$(.*?)\$\$', 'formula'),
            # LaTeX环境公式 \[...\]
            (r'\\\[(.*?)\\\]', 'formula'),
            # 行内公式 $...$
            (r'\$(.*?)\$', 'formula'),
        ]
        
        result = []
        last_end = 0
        
        # 遍历所有公式模式
        for pattern, type_ in patterns:
            matches = re.finditer(pattern, content, re.DOTALL)
            for match in matches:
                start, end = match.span()
                
                # 添加匹配前的文本
                if start > last_end:
                    text = content[last_end:start]
                    if text.strip():
                        result.append({'type': 'text', 'content': text})
                
                # 添加公式
                formula_content = match.group(1)
                result.append({'type': type_, 'content': formula_content})
                
                last_end = end
        
        # 添加剩余的文本
        if last_end < len(content):
            text = content[last_end:]
            if text.strip():
                result.append({'type': 'text', 'content': text})
        
        return result
    
    def _auto_wrap_text(self, text, max_chars=50):
        """
        自动换行处理，支持中英文混合文本
        
        参数:
            text: str - 要处理的文本
            max_chars: int - 每行最大字符数
        
        返回:
            list - 换行后的文本列表
        """
        lines = []
        current_line = []
        char_count = 0
        
        # 遍历文本中的每个字符
        for char in text:
            # 检查是否为换行符
            if char in ['\n', '\r']:
                # 添加当前行
                if current_line:
                    lines.append(''.join(current_line))
                    current_line = []
                    char_count = 0
                continue
            
            # 检查是否需要换行
            if char_count >= max_chars:
                # 添加当前行
                lines.append(''.join(current_line))
                current_line = []
                char_count = 0
            
            # 添加字符到当前行
            current_line.append(char)
            
            # 更新字符计数（中文字符计为1，英文字符计为0.5）
            if '\u4e00' <= char <= '\u9fff':
                # 中文字符
                char_count += 1
            else:
                # 英文字符
                char_count += 0.5
        
        # 添加最后一行
        if current_line:
            lines.append(''.join(current_line))
        
        return lines
    
    def _paginate_content(self, content_items, max_score=15):
        """
        根据内容分数自动分页
        
        参数:
            content_items: list - 包含文本和公式的列表
            max_score: int - 每页最大分数（普通行1分，公式行2分）
        
        返回:
            list - 分页后的内容列表，每个元素是一页的内容
        """
        pages = []
        current_page = []
        current_score = 0
        
        for item in content_items:
            if item['type'] == 'text':
                # 文本内容，需要换行处理
                wrapped_text = self._auto_wrap_text(item['content'])
                for line in wrapped_text:
                    line_score = 1  # 普通行1分
                    
                    # 检查是否超过当前页最大分数
                    if current_score + line_score > max_score:
                        # 开始新页
                        pages.append(current_page)
                        current_page = [{'type': 'text', 'content': line}]
                        current_score = line_score
                    else:
                        # 添加到当前页
                        current_page.append({'type': 'text', 'content': line})
                        current_score += line_score
            elif item['type'] == 'formula':
                # 公式内容，2分
                formula_score = 2
                
                # 检查是否超过当前页最大分数
                if current_score + formula_score > max_score:
                    # 开始新页
                    pages.append(current_page)
                    current_page = [{'type': 'formula', 'content': item['content']}]
                    current_score = formula_score
                else:
                    # 添加到当前页
                    current_page.append({'type': 'formula', 'content': item['content']})
                    current_score += formula_score
        
        # 添加最后一页
        if current_page:
            pages.append(current_page)
        
        return pages
    
    def _render_mixed_content(self, content_items, figsize, resolution, bg_color, text_color, randomness):
        """
        混合渲染：正文随机字体，公式传统渲染
        
        参数:
            content_items: list - 包含文本和公式的列表
            figsize: tuple - 图片尺寸（英寸）
            resolution: int - 图片分辨率（DPI）
            bg_color: str - 背景颜色
            text_color: str - 文字颜色
            randomness: float - 随机效果强度
        
        返回:
            PIL.Image - 渲染后的图片
        """
        # 转换英寸为像素
        width_px = int(figsize[0] * resolution)
        height_px = int(figsize[1] * resolution)
        
        # 创建空白图片
        img = Image.new('RGB', (width_px, height_px), bg_color)
        draw = ImageDraw.Draw(img)
        
        # 基本字体大小
        base_font_size = 48
        
        # 初始位置
        margin = int(width_px * 0.1)  # 10%边距
        x = margin
        y = margin + base_font_size
        line_height = int(base_font_size * 1.5)
        
        # 加载所有可用字体
        available_fonts = self.all_ttf_fonts
        
        # 系统黑体字体路径（用于中文）
        simhei_path = "C:/Windows/Fonts/simhei.ttf"
        
        # 处理每个内容项
        for item in content_items:
            if item['type'] == 'text':
                # 文本内容，每个字符随机字体
                for char in item['content']:
                    if char.isspace():
                        # 空格处理
                        x += int(base_font_size * 0.4)
                        continue
                    
                    try:
                        # 根据字符类型选择字体
                        if '\u4e00' <= char <= '\u9fff':
                            # 中文字符，使用系统黑体
                            if os.path.exists(simhei_path):
                                random_font_path = simhei_path
                            else:
                                # 如果没有找到黑体，随机选择一个字体
                                random_font_path = random.choice(available_fonts) if available_fonts else None
                        else:
                            # 英文字符，随机选择字体
                            random_font_path = random.choice(available_fonts) if available_fonts else None
                        
                        if random_font_path:
                            # 随机调整字体大小（±10%）
                            random_size = int(base_font_size * (0.9 + random.random() * 0.2))
                            
                            # 加载字体
                            pil_font = ImageFont.truetype(random_font_path, random_size)
                            
                            # 随机位置偏移
                            offset_x = int(random.uniform(-randomness*8, randomness*8))
                            offset_y = int(random.uniform(-randomness*8, randomness*8))
                            
                            # 绘制字符
                            draw.text((x + offset_x, y + offset_y), char, font=pil_font, fill=text_color)
                            
                            # 更新x坐标
                            char_width = pil_font.getbbox(char)[2] - pil_font.getbbox(char)[0]
                            x += char_width
                        else:
                            # 使用默认字体
                            draw.text((x, y), char, fill=text_color)
                            x += base_font_size * 0.6
                        
                        # 换行检查
                        if x > width_px - margin:
                            x = margin
                            y += line_height
                    except Exception as e:
                        # 如果字体加载失败，使用默认字体
                        draw.text((x, y), char, fill=text_color)
                        x += base_font_size * 0.6
                
                # 换行
                x = margin
                y += line_height
            elif item['type'] == 'formula':
                # 公式内容，使用传统渲染
                formula = item['content']
                
                # 创建临时图来渲染LaTeX公式
                temp_fig, temp_ax = plt.subplots(figsize=(8, 2), dpi=resolution)
                
                # 设置背景为透明
                temp_fig.patch.set_alpha(0)
                temp_ax.set_alpha(0)
                temp_ax.set_facecolor('none')
                
                # 渲染公式
                temp_ax.text(0.5, 0.5, f"${formula}$", fontsize=base_font_size, 
                            ha='center', va='center', color=text_color, 
                            transform=temp_ax.transAxes)
                
                # 隐藏坐标轴
                temp_ax.axis('off')
                
                # 保存临时图片到内存
                temp_buffer = BytesIO()
                temp_fig.savefig(temp_buffer, dpi=resolution, format='png', 
                                bbox_inches='tight', pad_inches=0.1, transparent=True)
                temp_buffer.seek(0)
                plt.close(temp_fig)
                
                # 读取临时图片
                formula_img = Image.open(temp_buffer)
                
                # 调整公式图片大小
                formula_width, formula_height = formula_img.size
                scale_factor = 0.8
                new_formula_width = int(formula_width * scale_factor)
                new_formula_height = int(formula_height * scale_factor)
                formula_img = formula_img.resize((new_formula_width, new_formula_height), Image.LANCZOS)
                
                # 计算公式位置
                formula_x = x
                formula_y = y - int(new_formula_height * 0.3)
                
                # 粘贴公式到主图片
                img.paste(formula_img, (formula_x, formula_y), formula_img)
                
                # 更新x坐标
                x += new_formula_width + int(base_font_size * 0.2)
                
                # 换行检查
                if x > width_px - margin:
                    x = margin
                    y += line_height
            
            # 检查是否超出页面高度
            if y > height_px - margin:
                break
        
        return img
    
    def _render_page(self, content_items, figsize, resolution, bg_color, text_color, randomness, mixed_rendering=False, random_fonts=False):
        """
        单页渲染，选择合适的渲染路径
        
        参数:
            content_items: list - 包含文本和公式的列表
            figsize: tuple - 图片尺寸（英寸）
            resolution: int - 图片分辨率（DPI）
            bg_color: str - 背景颜色
            text_color: str - 文字颜色
            randomness: float - 随机效果强度
            mixed_rendering: bool - 是否使用混合渲染
            random_fonts: bool - 是否每个字符随机使用不同字体
        
        返回:
            PIL.Image - 渲染后的图片
        """
        if mixed_rendering:
            # 使用混合渲染
            img = self._render_mixed_content(content_items, figsize, resolution, bg_color, text_color, randomness)
        elif random_fonts and self.all_ttf_fonts:
            # 使用随机字体渲染
            # 合并所有内容为纯文本
            pure_text = ''
            for item in content_items:
                if item['type'] == 'text':
                    pure_text += item['content'] + '\n'
                elif item['type'] == 'formula':
                    pure_text += f"${item['content']}$\n"
            
            # 使用随机字体渲染
            img = self._render_with_random_fonts(pure_text, resolution, False, figsize, bg_color, text_color, randomness)
        else:
            # 使用传统渲染
            # 创建一个临时图来渲染LaTeX
            fig, ax = plt.subplots(figsize=figsize, dpi=resolution)
            
            # 设置背景颜色
            fig.patch.set_facecolor(bg_color)
            ax.set_facecolor(bg_color)
            
            # 合并所有内容，使用$包裹公式
            pure_text = ''
            for item in content_items:
                if item['type'] == 'text':
                    pure_text += item['content'] + '\n'
                elif item['type'] == 'formula':
                    pure_text += f"${item['content']}$\n"
            
            # 设置matplotlib使用mathtext渲染公式
            plt.rcParams['text.usetex'] = False
            plt.rcParams['mathtext.fontset'] = 'stix'
            plt.rcParams['font.family'] = ['sans-serif']
            plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
            
            # 渲染LaTeX
            ax.text(0.5, 0.5, pure_text, fontsize=48, ha='center', va='center',
                    color=text_color, transform=ax.transAxes, linespacing=1.8)
            
            # 隐藏坐标轴
            ax.axis('off')
            
            # 调整边距
            plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
            
            # 保存临时图片到内存
            temp_buffer = BytesIO()
            plt.savefig(temp_buffer, dpi=resolution, format='png', bbox_inches='tight', pad_inches=0.1, transparent=(bg_color == 'transparent'))
            temp_buffer.seek(0)
            plt.close()
            
            # 读取临时图片
            img = Image.open(temp_buffer)
        
        # 添加手写效果
        if randomness > 0:
            img = self._add_handwriting_effect(img, randomness, text_color)
        
        return img
    
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
                 bg_color="white", text_color="black", format="png", a4=False,
                 markdown=False, random_fonts=False, mixed_rendering=False, max_chars=50, max_score=15):
    """便捷函数：将LaTeX公式转换为手写风格图片"""
    return _converter.convert_latex(latex, output_file, font, resolution, 
                                  width, height, randomness, bg_color, 
                                  text_color, format, a4, markdown, random_fonts, 
                                  mixed_rendering, max_chars, max_score)

def get_available_fonts():
    """获取可用的手写字体列表"""
    return list(_converter.available_fonts.keys())
