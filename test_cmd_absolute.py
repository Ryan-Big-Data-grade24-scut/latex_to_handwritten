#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试通过命令行工具使用绝对路径输出
"""

import os
import subprocess
import sys

def test_cmd_absolute():
    """测试通过命令行工具使用绝对路径输出"""
    print("测试通过命令行工具使用绝对路径输出...")
    
    # 创建测试内容文件，包含足够多的行确保生成多页
    test_content = """
测试内容第一行。
测试内容第二行。
测试内容第三行。
测试内容第四行。
测试内容第五行。
测试内容第六行。
测试内容第七行。
测试内容第八行。
测试内容第九行。
测试内容第十行。
测试内容第十一行。
测试内容第十二行。
测试内容第十三行。
测试内容第十四行。
测试内容第十五行。
测试内容第十六行。
测试内容第十七行。
测试内容第十八行。
测试内容第十九行。
测试内容第二十行。
"""
    test_file = r"e:\Ufolder\Current\ActionSys\TempProgram\latex_to_handwritten\test_cmd_content.txt"
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    # 测试：使用命令行工具和绝对路径输出
    print("\n测试：使用命令行工具和绝对路径输出")
    output_path = r"e:\Ufolder\Current\ActionSys\TempProgram\latex_to_handwritten\test_cmd_output.png"
    
    try:
        # 构建命令，使用足够长的内容确保生成多页
        cmd = [
            sys.executable, 'main.py',
            '-i', test_file,
            '-o', output_path,
            '--a4'
        ]
        
        print(f"执行命令：{' '.join(cmd)}")
        
        # 执行命令
        result = subprocess.run(cmd, cwd=r"e:\Ufolder\Current\ActionSys\TempProgram\latex_to_handwritten", 
                              capture_output=True, text=True, encoding='utf-8')
        
        print(f"命令退出码：{result.returncode}")
        print(f"标准输出：{result.stdout}")
        if result.stderr:
            print(f"标准错误：{result.stderr}")
        
        # 检查生成的文件
        generated_files = []
        base_name, ext = os.path.splitext(output_path)
        
        # 查找所有生成的页面文件
        i = 1
        while True:
            if i == 1:
                file_path = output_path
            else:
                file_path = f"{base_name}_page_{i}{ext}"
            
            if os.path.exists(file_path):
                generated_files.append(file_path)
                i += 1
            else:
                break
        
        if generated_files:
            print(f"\n✓ 命令执行成功！生成的文件：")
            for file in generated_files:
                print(f"  - {file}")
                # 验证文件是否保存在指定的绝对路径下
                expected_dir = os.path.dirname(output_path)
                actual_dir = os.path.dirname(file)
                if actual_dir == expected_dir:
                    print(f"    ✅ 文件保存在正确的绝对路径目录")
                else:
                    print(f"    ❌ 文件保存在错误目录：{actual_dir}")
        else:
            print("\n✗ 没有生成任何文件！")
        
        # 清理测试文件
        print("\n清理测试文件：")
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"  - 已清理测试内容文件：{test_file}")
            
        for file in generated_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"  - 已清理输出文件：{file}")
                
    except Exception as e:
        print(f"✗ 测试失败：{e}")
        import traceback
        traceback.print_exc()
    
    print("\n测试完成！")

if __name__ == "__main__":
    test_cmd_absolute()