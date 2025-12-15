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
# 关键：启用mathtext的LaTeX语法支持
plt.rcParams['text.usetex'] = False
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['mathtext.rm'] = 'serif'
plt.rcParams['mathtext.it'] = 'serif:italic'
plt.rcParams['mathtext.bf'] = 'serif:bold'

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
                     markdown=False, random_fonts=False, mixed_rendering=False,
                     process_latex_markers=False, max_chars=50, max_score=15):
        """
        将LaTeX公式转换为手写风格图片
        
        参数:
            latex: str - LaTeX公式字符串，支持多行
            output_file: str - 输出文件路径或文件夹
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
            process_latex_markers: bool - 是否处理LaTeX标记
            max_chars: int - 每行最大字符数
            max_score: int - 每页最大分数（普通行1分，公式行2分）
        """
        # 加载配置
        from config_manager import get_default_config
        config = get_default_config()
        
        # 使用配置中的默认值（如果参数未指定）
        if max_chars is None:
            max_chars = config.get('max_chars', 50)
        if max_score is None:
            max_score = config.get('max_score', 15)
        
        # 关键修复：确保反斜杠被正确处理，防止\f被解释为换页符
        # 无需额外处理，因为文件读取时已经正确处理了反斜杠
        
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
        
        # 检测文本中是否包含公式
        has_formulas = False
        
        # 检查是否包含公式标记
        if '$' in latex or '\\frac' in latex or '\\sum' in latex or '\\int' in latex or '\\lim' in latex:
            has_formulas = True
        
        # 自动换行处理
        latex = self._auto_wrap_text(latex, max_chars=max_chars)
        
        # 分页处理
        pages = self._paginate_content(latex, max_score=max_score)
        
        # 检查输出路径是文件还是文件夹
        output_files = []
        
        # 检查是否为文件夹输出：如果没有扩展名或路径已存在为目录
        is_folder_output = False
        file_ext = os.path.splitext(output_file)[1]
        
        # 如果路径已存在且是目录，或者没有扩展名，视为文件夹输出
        if os.path.isdir(output_file) or not file_ext:
            is_folder_output = True
        
        if is_folder_output:
            # 输出到文件夹
            # 确保文件夹存在
            os.makedirs(output_file, exist_ok=True)
            folder_name = os.path.basename(output_file)
            for i, page_content in enumerate(pages):
                page_output_file = os.path.join(output_file, f"{folder_name}_page{i+1}.{format}")
                output_files.append(self._render_page(page_content, page_output_file, font, resolution, a4, figsize, bg_color, text_color, randomness, format, has_formulas, random_fonts, mixed_rendering))
        else:
            # 输出到单个文件（只渲染第一页）
            if pages:
                output_files.append(self._render_page(pages[0], output_file, font, resolution, a4, figsize, bg_color, text_color, randomness, format, has_formulas, random_fonts, mixed_rendering))
        
        return output_files[0] if output_files else None
    
    def _auto_wrap_text(self, text, max_chars=30):
        """
        自动换行处理：普通文本每行不超过max_chars个字符，公式不单独换行
        """
        if not text:
            return text
        
        # 先按显式换行符分割文本，保留原始换行语义
        lines = text.split('\n')
        final_result = []
        
        for line in lines:
            # 分割当前行的文本和公式
            content_parts = self._split_text_formulas(line)
            
            wrapped_line = []
            current_line = ""
            
            for part_type, content in content_parts:
                if part_type == 'text':
                    # 处理普通文本，支持中文和英文
                    if content.strip():
                        # 检查是否有空格（英文文本）
                        if ' ' in content:
                            # 英文文本，按空格分割单词
                            words = content.split()
                            for word in words:
                                if len(current_line + word + " ") <= max_chars:
                                    current_line += word + " "
                                else:
                                    if current_line:
                                        wrapped_line.append(current_line.strip())
                                    current_line = word + " "
                        else:
                            # 中文文本，按字符分割
                            for char in content:
                                if len(current_line + char) <= max_chars:
                                    current_line += char
                                else:
                                    if current_line:
                                        wrapped_line.append(current_line.strip())
                                    current_line = char
                else:
                    # 处理公式，不单独换行，直接添加到当前行
                    # 检查是否需要换行
                    if len(current_line + content + " ") <= max_chars:
                        # 如果当前行加上公式不会超过最大字符数，直接添加
                        current_line += content + " "
                    else:
                        # 否则先添加当前行，然后开始新行
                        if current_line:
                            wrapped_line.append(current_line.strip())
                        current_line = content + " "
            
            if current_line:
                wrapped_line.append(current_line.strip())
            
            # 将当前行的处理结果添加到最终结果
            final_result.extend(wrapped_line)
        
        return "\n".join(final_result)
    
    def _paginate_content(self, text, max_score=15):
        """
        分页处理：普通字符每行1分，公式每行2分，大于max_score自动分页
        """
        if not text:
            return [""]
        
        lines = text.split("\n")
        pages = []
        current_page = []
        current_score = 0
        
        for line in lines:
            if line.strip():
                # 计算行分数
                if '$' in line:
                    line_score = 2  # 公式行2分
                else:
                    line_score = 1  # 普通文本行1分
                
                # 检查是否需要分页
                if current_score + line_score > max_score:
                    # 分页
                    pages.append("\n".join(current_page))
                    current_page = [line]
                    current_score = line_score
                else:
                    # 添加到当前页
                    current_page.append(line)
                    current_score += line_score
            else:
                # 空行不计分，直接添加
                current_page.append(line)
        
        # 添加最后一页
        if current_page:
            pages.append("\n".join(current_page))
        
        return pages
    
    def _render_page(self, latex, output_file, font, resolution, a4, figsize, bg_color, text_color, randomness, format, has_formulas, random_fonts, mixed_rendering):
        """
        渲染单页内容
        """
        # 初始化img变量
        img = None
        
        # 渲染路径选择
        if mixed_rendering and has_formulas:
            # 路径3：混合渲染，正文随机字体，公式传统渲染
            # 关键修复：先处理latex文本中的反斜杠问题
            latex = latex.replace('\x0c', '\\f')
            img = self._render_mixed_content(latex, resolution, a4, figsize, bg_color, text_color, randomness)
        elif random_fonts and self.all_ttf_fonts and not has_formulas:
            # 路径1：纯文本，使用随机字体渲染
            img = self._render_with_random_fonts(latex, resolution, a4, figsize, bg_color, text_color, randomness)
        else:
            # 路径2：包含公式或不使用随机字体，使用传统渲染
            # 关键修复：先处理latex文本中的反斜杠问题
            latex = latex.replace('\x0c', '\\f')
            
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
                
                # 关键修复：使用stix字体集确保公式正确显示
                plt.rcParams['mathtext.fontset'] = 'stix'
                plt.rcParams['mathtext.rm'] = 'stixregular'
                plt.rcParams['mathtext.it'] = 'stixitalic'
                plt.rcParams['mathtext.bf'] = 'stixbold'
            else:
                # 关键修复：使用stix字体集确保公式正确显示
                plt.rcParams['mathtext.fontset'] = 'stix'
                plt.rcParams['mathtext.rm'] = 'stixregular'
                plt.rcParams['mathtext.it'] = 'stixitalic'
                plt.rcParams['mathtext.bf'] = 'stixbold'
            
            # 创建一个临时图来渲染LaTeX
            fig, ax = plt.subplots(figsize=figsize, dpi=resolution)
            
            # 设置背景颜色
            fig.patch.set_facecolor(bg_color)
            ax.set_facecolor(bg_color)
            
            # 渲染LaTeX公式（支持多行）
            # 将\n替换为换行符，支持多行输入
            latex = latex.replace('\\n', '\n')
            
            # 根据内容类型调整字体大小，使其更整齐
            if '\\frac' in latex or '\\sum' in latex or '\\int' in latex or '\\max' in latex:
                font_size = 36
            else:
                font_size = 48
                
            if a4:
                font_size = 42
                
            ax.text(0.5, 0.5, latex, fontsize=font_size, ha='center', va='center',
                    color=text_color, transform=ax.transAxes, linespacing=1.8)
            
            # 隐藏坐标轴
            ax.axis('off')
            
            # 直接使用subplots_adjust调整边距，避免tight_layout警告
            plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
            
            # 保存临时图片到内存
            temp_buffer = BytesIO()
            plt.savefig(temp_buffer, dpi=resolution, format='png', bbox_inches='tight', pad_inches=0.1, transparent=(bg_color == 'transparent'))
            temp_buffer.seek(0)
            plt.close()
            
            # 读取临时图片
            img = Image.open(temp_buffer)
        
        # 添加手写效果，调整随机强度使其更整齐
        if randomness > 0:
            img = self._add_handwriting_effect(img, randomness * 0.7, text_color)  # 降低随机强度，使其更整齐
        
        # 保存最终图片
        img.save(output_file, format=format)
        
        return output_file
    
    def _split_text_formulas(self, text):
        """
        将文本分割为正文和公式部分
        返回格式：[(type, content), ...]，type为'text'或'formula'
        """
        parts = []
        
        # 关键修复：使用更简单可靠的方式提取公式
        # 先处理行内公式 $...$
        # 先处理块级公式 $$...$$
        # 使用非贪婪匹配，确保正确分割
        
        # 特殊处理：将可能被错误解释的\f等替换回正确的\frac形式
        text = text.replace('\x0c', '\\f')  # 修复\f被解释为换页符的问题
        
        # 匹配所有公式类型
        # 注意：使用原始字符串r前缀，确保正则表达式正确处理反斜杠
        formula_pattern = r'(\$\$.*?\$\$)|(\$[^$\n]*?\$)'  # 只匹配$和$$公式
        
        last_end = 0
        for match in re.finditer(formula_pattern, text, re.DOTALL):
            # 正文部分
            if match.start() > last_end:
                parts.append(('text', text[last_end:match.start()]))
            
            # 公式部分
            formula_content = match.group()
            parts.append(('formula', formula_content))
            
            last_end = match.end()
        
        # 剩余正文
        if last_end < len(text):
            parts.append(('text', text[last_end:]))
        
        return parts
    
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
                    
                    # 随机调整字体大小（±10%），减少随机性
                    random_size = int(base_font_size * (0.95 + random.random() * 0.1))
                    
                    # 加载字体
                    pil_font = ImageFont.truetype(random_font_path, random_size)
                    
                    # 随机位置偏移，减少偏移量
                    offset_x = int(random.uniform(-randomness*4, randomness*4))
                    offset_y = int(random.uniform(-randomness*2, randomness*2))
                    
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
    
    def _render_mixed_content(self, latex, resolution, a4, figsize, bg_color, text_color, randomness):
        """
        混合渲染：正文使用随机字体，公式使用传统渲染
        """
        # 转换英寸为像素
        width_px = int(figsize[0] * resolution)
        height_px = int(figsize[1] * resolution)
        
        # 创建空白图片作为最终输出
        final_img = Image.new('RGB', (width_px, height_px), bg_color)
        draw = ImageDraw.Draw(final_img)
        
        # 分割文本和公式
        content_parts = self._split_text_formulas(latex)
        
        if not content_parts:
            return final_img
        
        # 基本字体大小和位置
        base_font_size = 48 if not a4 else 42
        margin = int(width_px * 0.1)  # 10%边距
        x = margin
        y = margin + base_font_size
        line_height = base_font_size * 1.8
        
        # 处理每个内容部分
        for part_type, content in content_parts:
            # 先处理转义字符
            content = content.replace('\\n', '\n')
            if part_type == 'text':
                # 正文部分，使用随机字体渲染
                if not content.strip():
                    y += line_height
                    x = margin
                    continue
                
                # 处理每行文本
                lines = content.split('\n')
                for line in lines:
                    if not line.strip():
                        y += line_height
                        x = margin
                        continue
                    
                    # 处理行中的每个字符
                    for char in line:
                        if char.isspace():
                            x += base_font_size * 0.4
                            continue
                        
                        try:
                            # 选择合适的字体
                            font_path = None
                            # 中文处理：使用支持中文的字体
                            if '\u4e00' <= char <= '\u9fff':
                                # 中文字符，使用系统黑体字体
                                font_path = 'C:\\Windows\\Fonts\\simhei.ttf'  # Windows系统黑体字体
                            else:
                                # 英文字符，随机选择字体
                                font_path = random.choice(self.all_ttf_fonts)
                        
                            # 随机调整字体大小（±10%），减少随机性
                            random_size = int(base_font_size * (0.95 + random.random() * 0.1))
                            
                            # 加载字体
                            pil_font = ImageFont.truetype(font_path, random_size)
                            
                            # 随机位置偏移，减少偏移量
                            offset_x = int(random.uniform(-randomness*4, randomness*4))
                            offset_y = int(random.uniform(-randomness*2, randomness*2))
                            
                            # 直接绘制字符到主图片
                            draw.text((x + offset_x, y + offset_y), char, font=pil_font, fill=text_color)
                            
                            # 使用固定宽度估计，避免bbox问题
                            char_width = random_size * 0.6
                            
                            # 更新x坐标
                            x += char_width
                            
                            # 换行检查
                            if x > width_px - margin:
                                x = margin
                                y += line_height
                                break
                        except Exception as e:
                            # 如果字体加载失败，使用默认字体大小
                            draw.text((x, y), char, font=ImageFont.load_default(), fill=text_color)
                            x += base_font_size * 0.5
                    
                    # 换行
                    x = margin
                    y += line_height
                    
                    # 检查是否超出页面高度
                    if y > height_px - margin:
                        break
            else:
                # 公式部分，使用传统渲染
                if not content.strip():
                    continue
                
                # 临时渲染公式，移除公式标记
                # 移除$、$$或\[\]标记
                clean_formula = content
                if clean_formula.startswith('$$') and clean_formula.endswith('$$'):
                    clean_formula = clean_formula[2:-2]
                elif clean_formula.startswith('$') and clean_formula.endswith('$'):
                    clean_formula = clean_formula[1:-1]
                elif clean_formula.startswith('\\[') and clean_formula.endswith('\\]'):
                    clean_formula = clean_formula[2:-2]
                
                formula_img = self._render_with_traditional(clean_formula, resolution, a4, 
                                                          (figsize[0] * 0.8, figsize[1] * 0.2), 
                                                          bg_color, text_color)
                
                # 调整公式图片大小，使其适合当前行
                formula_width, formula_height = formula_img.size
                scale_factor = min((width_px - 2 * margin) / formula_width, 0.5)  # 限制最大缩放
                new_formula_width = int(formula_width * scale_factor)
                new_formula_height = int(formula_height * scale_factor)
                
                formula_img = formula_img.resize((new_formula_width, new_formula_height), 
                                               Image.Resampling.LANCZOS)
                
                # 计算公式位置
                formula_x = int(x if x > margin else margin)
                formula_y = int(y - new_formula_height * 0.3)  # 垂直居中对齐
                
                # 检查是否需要换行
                if formula_x + new_formula_width > width_px - margin:
                    x = margin
                    y += line_height
                    formula_x = int(x)
                    formula_y = int(y - new_formula_height * 0.3)
                
                # 粘贴公式到最终图片
                final_img.paste(formula_img, (formula_x, formula_y), formula_img.convert('RGBA'))
                
                # 更新位置
                x = formula_x + new_formula_width + int(base_font_size * 0.4)
                
                # 如果公式宽度超过一行，换行
                if x > width_px - margin:
                    x = margin
                    y += line_height + new_formula_height * 0.5
            
        return final_img
    
    def _render_with_traditional(self, latex, resolution, a4, figsize, bg_color, text_color):
        """
        使用传统的matplotlib渲染，公式使用LaTeX语法渲染
        """
        # 关键：不覆盖全局的LaTeX配置，使用已设置的cm字体集
        # 保持全局配置不变，确保LaTeX语法正确解析
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 确保使用正确的数学字体配置，解决公式显示问题
        plt.rcParams['mathtext.fontset'] = 'stix'
        plt.rcParams['mathtext.rm'] = 'stixregular'
        plt.rcParams['mathtext.it'] = 'stixitalic'
        plt.rcParams['mathtext.bf'] = 'stixbold'
        
        # 额外修复：确保公式中的\frac正确显示
        latex = latex.replace('\x0c', '\\f')
        
        # 创建一个临时图来渲染LaTeX
        fig, ax = plt.subplots(figsize=figsize, dpi=resolution)
        
        # 设置背景颜色
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        
        # 渲染LaTeX公式（支持多行）
        # 将\n替换为换行符，支持多行输入
        latex = latex.replace('\\n', '\n')
        
        # 根据内容类型调整字体大小
        font_size = 48 if not a4 else 42
        
        # 渲染文本
        ax.text(0.5, 0.5, latex, fontsize=font_size, ha='center', va='center',
                color=text_color, transform=ax.transAxes, linespacing=1.8)
        
        # 隐藏坐标轴
        ax.axis('off')
        
        # 直接使用subplots_adjust调整边距，避免tight_layout警告
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        
        # 保存临时图片到内存
        temp_buffer = BytesIO()
        plt.savefig(temp_buffer, dpi=resolution, format='png', bbox_inches='tight', pad_inches=0.1, transparent=(bg_color == 'transparent'))
        temp_buffer.seek(0)
        plt.close()
        
        # 读取临时图片
        img = Image.open(temp_buffer)
        
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
                    # 应用随机偏移，减少偏移量
                    offset_x = int(random.uniform(-randomness*3, randomness*3))
                    offset_y = int(random.uniform(-randomness*2, randomness*2))
                    
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
                 bg_color="white", text_color="black", format="png", a4=False,
                 markdown=False, random_fonts=False, mixed_rendering=False):
    """便捷函数：将LaTeX公式转换为手写风格图片"""
    return _converter.convert_latex(latex, output_file, font, resolution, 
                                  width, height, randomness, bg_color, 
                                  text_color, format, a4, markdown, random_fonts, mixed_rendering)

def get_available_fonts():
    """获取可用的手写字体列表"""
    return list(_converter.available_fonts.keys())
