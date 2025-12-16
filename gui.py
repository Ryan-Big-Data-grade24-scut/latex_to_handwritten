import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from latex2handwritten import convert_latex
from process_latex_markers import process_latex_markers
from config_manager import config_manager, get_all_presets

class LatexToHandwrittenGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LaTeX to Handwritten Converter")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置主题
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置样式
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('TCheckbutton', font=('Arial', 10))
        style.configure('TCombobox', font=('Arial', 10))
        style.configure('TLabelframe.Label', font=('Arial', 11, 'bold'))
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 预设配置部分
        preset_frame = ttk.Labelframe(main_frame, text="Presets", padding="10")
        preset_frame.pack(fill=tk.X, pady=5)
        
        preset_row = ttk.Frame(preset_frame)
        preset_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(preset_row, text="Select Preset:").pack(side=tk.LEFT, padx=5)
        self.preset_var = tk.StringVar(value="default")
        self.preset_combo = ttk.Combobox(preset_row, textvariable=self.preset_var, values=["default"] + get_all_presets(), state="readonly")
        self.preset_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.load_preset_btn = ttk.Button(preset_row, text="Load Preset", command=self.load_preset)
        self.load_preset_btn.pack(side=tk.RIGHT, padx=5)
        
        # 1. 输入部分
        input_frame = ttk.Labelframe(main_frame, text="Input", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        # 输入方式选择
        input_type_frame = ttk.Frame(input_frame)
        input_type_frame.pack(fill=tk.X, pady=5)
        
        self.input_type = tk.StringVar(value="direct")
        
        direct_input_rb = ttk.Radiobutton(input_type_frame, text="Direct Input", variable=self.input_type, value="direct", command=self.toggle_input_type)
        direct_input_rb.pack(side=tk.LEFT, padx=10)
        
        file_input_rb = ttk.Radiobutton(input_type_frame, text="File Input", variable=self.input_type, value="file", command=self.toggle_input_type)
        file_input_rb.pack(side=tk.LEFT, padx=10)
        
        # 直接输入
        self.direct_input_frame = ttk.Frame(input_frame)
        self.direct_input_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.latex_input = tk.Text(self.direct_input_frame, height=10, wrap=tk.WORD, font=('Arial', 10))
        self.latex_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 文件输入
        self.file_input_frame = ttk.Frame(input_frame)
        self.file_input_frame.pack(fill=tk.X, pady=5)
        self.file_input_frame.pack_forget()
        
        file_input_row = ttk.Frame(self.file_input_frame)
        file_input_row.pack(fill=tk.X, pady=5)
        
        self.file_path_var = tk.StringVar()
        self.file_path_entry = ttk.Entry(file_input_row, textvariable=self.file_path_var, width=50, state="readonly")
        self.file_path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.browse_file_btn = ttk.Button(file_input_row, text="Browse", command=self.browse_file)
        self.browse_file_btn.pack(side=tk.RIGHT, padx=5)
        
        # 2. 输出部分
        output_frame = ttk.Labelframe(main_frame, text="Output", padding="10")
        output_frame.pack(fill=tk.X, pady=5)
        
        # 输出类型选择
        output_type_row = ttk.Frame(output_frame)
        output_type_row.pack(fill=tk.X, pady=5)
        
        self.output_type = tk.StringVar(value="file")
        
        file_output_rb = ttk.Radiobutton(output_type_row, text="File Output", variable=self.output_type, value="file", command=self.toggle_output_type)
        file_output_rb.pack(side=tk.LEFT, padx=10)
        
        folder_output_rb = ttk.Radiobutton(output_type_row, text="Folder Output (Multi-page)", variable=self.output_type, value="folder", command=self.toggle_output_type)
        folder_output_rb.pack(side=tk.LEFT, padx=10)
        
        # 输出路径
        output_path_row = ttk.Frame(output_frame)
        output_path_row.pack(fill=tk.X, pady=5)
        
        self.output_path_var = tk.StringVar(value="output.png")
        self.output_path_entry = ttk.Entry(output_path_row, textvariable=self.output_path_var, width=50)
        self.output_path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.browse_output_btn = ttk.Button(output_path_row, text="Browse", command=self.browse_output)
        self.browse_output_btn.pack(side=tk.RIGHT, padx=5)
        
        # 3. 渲染选项
        render_frame = ttk.Labelframe(main_frame, text="Rendering Options", padding="10")
        render_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 左侧选项
        left_options = ttk.Frame(render_frame)
        left_options.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # 字体选择
        font_row = ttk.Frame(left_options)
        font_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(font_row, text="Font:").pack(side=tk.LEFT, padx=5)
        self.font_var = tk.StringVar(value="IndieFlower-Regular")
        self.font_combo = ttk.Combobox(font_row, textvariable=self.font_var, values=["IndieFlower-Regular", "Caveat-Bold", "Caveat-Regular", "ArchitectsDaughter-Regular", "ReenieBeanie-Regular"], state="readonly")
        self.font_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 分辨率
        resolution_row = ttk.Frame(left_options)
        resolution_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(resolution_row, text="Resolution:").pack(side=tk.LEFT, padx=5)
        self.resolution_var = tk.IntVar(value=200)
        self.resolution_spinbox = ttk.Spinbox(resolution_row, from_=100, to=600, increment=50, textvariable=self.resolution_var)
        self.resolution_spinbox.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Label(resolution_row, text="DPI").pack(side=tk.LEFT, padx=5)
        
        # 随机效果强度
        randomness_row = ttk.Frame(left_options)
        randomness_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(randomness_row, text="Randomness:").pack(side=tk.LEFT, padx=5)
        self.randomness_var = tk.DoubleVar(value=0.05)
        self.randomness_scale = ttk.Scale(randomness_row, from_=0.0, to=1.0, orient=tk.HORIZONTAL, variable=self.randomness_var, length=150)
        self.randomness_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.randomness_label = ttk.Label(randomness_row, text="0.05")
        self.randomness_label.pack(side=tk.LEFT, padx=5)
        self.randomness_scale.bind("<Motion>", self.update_randomness_label)
        
        # 每行最大字符数
        max_chars_row = ttk.Frame(left_options)
        max_chars_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(max_chars_row, text="Max Chars per Line:").pack(side=tk.LEFT, padx=5)
        self.max_chars_var = tk.IntVar(value=50)
        self.max_chars_spinbox = ttk.Spinbox(max_chars_row, from_=10, to=200, increment=5, textvariable=self.max_chars_var)
        self.max_chars_spinbox.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 每页最大分数
        max_score_row = ttk.Frame(left_options)
        max_score_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(max_score_row, text="Max Score per Page:").pack(side=tk.LEFT, padx=5)
        self.max_score_var = tk.IntVar(value=15)
        self.max_score_spinbox = ttk.Spinbox(max_score_row, from_=5, to=50, increment=5, textvariable=self.max_score_var)
        self.max_score_spinbox.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 右侧选项
        right_options = ttk.Frame(render_frame)
        right_options.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # 复选框选项
        self.a4_var = tk.BooleanVar(value=False)
        a4_check = ttk.Checkbutton(right_options, text="A4 Format", variable=self.a4_var)
        a4_check.pack(anchor=tk.W, pady=5)
        
        self.markdown_var = tk.BooleanVar(value=False)
        markdown_check = ttk.Checkbutton(right_options, text="Markdown Support", variable=self.markdown_var)
        markdown_check.pack(anchor=tk.W, pady=5)
        
        self.random_fonts_var = tk.BooleanVar(value=False)
        random_fonts_check = ttk.Checkbutton(right_options, text="Random Fonts per Character", variable=self.random_fonts_var)
        random_fonts_check.pack(anchor=tk.W, pady=5)
        
        self.mixed_rendering_var = tk.BooleanVar(value=False)
        mixed_rendering_check = ttk.Checkbutton(right_options, text="Mixed Rendering", variable=self.mixed_rendering_var)
        mixed_rendering_check.pack(anchor=tk.W, pady=5)
        
        self.process_latex_markers_var = tk.BooleanVar(value=False)
        process_latex_markers_check = ttk.Checkbutton(right_options, text="Process LaTeX Markers", variable=self.process_latex_markers_var)
        process_latex_markers_check.pack(anchor=tk.W, pady=5)
        
        # 4. 执行按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=15)
        
        self.convert_btn = ttk.Button(button_frame, text="Convert", command=self.convert)
        self.convert_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear)
        self.clear_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 5. 状态显示
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=5)
        status_label.pack(fill=tk.X)
    
    def toggle_input_type(self):
        """切换输入方式"""
        if self.input_type.get() == "direct":
            self.direct_input_frame.pack(fill=tk.BOTH, expand=True, pady=5)
            self.file_input_frame.pack_forget()
        else:
            self.direct_input_frame.pack_forget()
            self.file_input_frame.pack(fill=tk.X, pady=5)
    
    def browse_file(self):
        """浏览输入文件"""
        file_path = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[("Text Files", "*.txt"), ("Markdown Files", "*.md"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
    
    def toggle_output_type(self):
        """切换输出类型"""
        if self.output_type.get() == "file":
            self.output_path_var.set("output.png")
        else:
            self.output_path_var.set("output_folder")
    
    def browse_output(self):
        """浏览输出文件或文件夹"""
        if self.output_type.get() == "file":
            # 浏览输出文件
            file_path = filedialog.asksaveasfilename(
                title="Save Output Image",
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png"), ("JPG Files", "*.jpg"), ("SVG Files", "*.svg")]
            )
            if file_path:
                self.output_path_var.set(file_path)
        else:
            # 浏览输出文件夹
            folder_path = filedialog.askdirectory(title="Select Output Folder")
            if folder_path:
                self.output_path_var.set(folder_path)
    
    def update_randomness_label(self, event):
        """更新随机效果强度标签"""
        value = round(self.randomness_var.get(), 2)
        self.randomness_label.config(text=str(value))
    
    def convert(self):
        """执行转换"""
        try:
            # 获取输入内容
            if self.input_type.get() == "direct":
                latex_content = self.latex_input.get("1.0", tk.END).strip()
                if not latex_content:
                    messagebox.showerror("Error", "Please enter some LaTeX content")
                    return
            else:
                file_path = self.file_path_var.get()
                if not file_path:
                    messagebox.showerror("Error", "Please select an input file")
                    return
                with open(file_path, 'r', encoding='utf-8') as f:
                    latex_content = f.read().strip()
                if not latex_content:
                    messagebox.showerror("Error", "The selected file is empty")
                    return
            
            # 获取输出路径
            output_path = self.output_path_var.get()
            if not output_path:
                messagebox.showerror("Error", "Please enter an output path")
                return
            
            # 提取输出格式
            if self.output_type.get() == "file":
                format = os.path.splitext(output_path)[1][1:]  # 移除点号
                if not format:
                    format = "png"  # 默认格式
            else:
                format = "png"  # 文件夹输出默认使用png格式
            
            # 获取其他参数
            font = self.font_var.get()
            resolution = self.resolution_var.get()
            randomness = self.randomness_var.get()
            a4 = self.a4_var.get()
            markdown = self.markdown_var.get()
            random_fonts = self.random_fonts_var.get()
            mixed_rendering = self.mixed_rendering_var.get()
            process_markers = self.process_latex_markers_var.get()
            
            # 处理LaTeX标记
            if process_markers:
                latex_content = process_latex_markers(latex_content)
            
            # 更新状态
            self.status_var.set("Converting...")
            self.root.update()
            
            # 执行转换
            if self.output_type.get() == "folder":
                # 确保输出文件夹存在
                os.makedirs(output_path, exist_ok=True)
            
            # 获取分页参数
            max_chars = self.max_chars_var.get()
            max_score = self.max_score_var.get()
            
            output_files = convert_latex(
                latex=latex_content,
                output_file=output_path,
                font=font,
                resolution=resolution,
                randomness=randomness,
                a4=a4,
                markdown=markdown,
                random_fonts=random_fonts,
                mixed_rendering=mixed_rendering,
                format=format,  # 传递格式参数
                max_chars=max_chars,  # 传递每行最大字符数
                max_score=max_score  # 传递每页最大分数
            )
            
            # 更新状态
            if self.output_type.get() == "file":
                self.status_var.set(f"Successfully converted to: {output_files}")
                messagebox.showinfo("Success", f"Successfully converted to: {output_files}")
            else:
                self.status_var.set(f"Successfully converted to folder: {output_path}")
                messagebox.showinfo("Success", f"Successfully converted to folder: {output_path}")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def load_preset(self):
        """加载预设配置"""
        preset_name = self.preset_var.get()
        
        # 获取预设配置
        if preset_name == "default":
            preset_config = config_manager.get_default_config()
        else:
            preset_config = config_manager.get_preset(preset_name)
        
        # 更新GUI控件
        if "font" in preset_config:
            self.font_var.set(preset_config["font"])
        if "resolution" in preset_config:
            self.resolution_var.set(preset_config["resolution"])
        if "randomness" in preset_config:
            self.randomness_var.set(preset_config["randomness"])
            self.randomness_label.config(text=str(round(preset_config["randomness"], 2)))
        if "a4" in preset_config:
            self.a4_var.set(preset_config["a4"])
        if "markdown" in preset_config:
            self.markdown_var.set(preset_config["markdown"])
        if "random_fonts" in preset_config:
            self.random_fonts_var.set(preset_config["random_fonts"])
        if "mixed_rendering" in preset_config:
            self.mixed_rendering_var.set(preset_config["mixed_rendering"])
        if "process_latex_markers" in preset_config:
            self.process_latex_markers_var.set(preset_config["process_latex_markers"])
        if "max_chars" in preset_config:
            self.max_chars_var.set(preset_config["max_chars"])
        if "max_score" in preset_config:
            self.max_score_var.set(preset_config["max_score"])
        
        self.status_var.set(f"Loaded preset: {preset_name}")
        messagebox.showinfo("Success", f"Successfully loaded preset: {preset_name}")
    
    def clear(self):
        """清除输入和重置选项"""
        self.latex_input.delete("1.0", tk.END)
        self.file_path_var.set("")
        self.output_path_var.set("output.png")
        self.font_var.set("IndieFlower-Regular")
        self.resolution_var.set(200)
        self.randomness_var.set(0.05)
        self.randomness_label.config(text="0.05")
        self.a4_var.set(False)
        self.markdown_var.set(False)
        self.random_fonts_var.set(False)
        self.mixed_rendering_var.set(False)
        self.process_latex_markers_var.set(False)
        self.max_chars_var.set(50)  # 重置每行最大字符数到默认值
        self.max_score_var.set(15)  # 重置每页最大分数到默认值
        self.status_var.set("Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = LatexToHandwrittenGUI(root)
    root.mainloop()