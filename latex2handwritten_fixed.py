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
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['mathtext.rm'] = 'stixregular'
plt.rcParams['mathtext.it'] = 'stixitalic'
plt.rcParams['mathtext.bf'] = 'stixbold'

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
        
