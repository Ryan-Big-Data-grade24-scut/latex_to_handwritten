import os
import shutil
from config_manager import config_manager

def test_config_loading():
    """测试配置参数加载是否正确"""
    print("测试配置参数加载...")
    
    # 获取默认配置
    default_config = config_manager.get_default_config()
    print(f"  默认配置: max_chars={default_config['max_chars']}, max_score={default_config['max_score']}")
    
    # 获取all_enabled预设配置
    all_enabled_config = config_manager.get_preset("all_enabled")
    print(f"  all_enabled预设: max_chars={all_enabled_config['max_chars']}, max_score={all_enabled_config['max_score']}")
    
    # 验证配置是否与config.json一致
    if default_config['max_chars'] == 50 and default_config['max_score'] == 15:
        print("  正确：默认配置加载正确")
    else:
        print(f"  错误：默认配置加载错误，期望 max_chars=50, max_score=15，实际得到 max_chars={default_config['max_chars']}, max_score={default_config['max_score']}")
    
    if all_enabled_config['max_chars'] == 30 and all_enabled_config['max_score'] == 25:
        print("  正确：all_enabled预设加载正确")
    else:
        print(f"  错误：all_enabled预设加载错误，期望 max_chars=30, max_score=25，实际得到 max_chars={all_enabled_config['max_chars']}, max_score={all_enabled_config['max_score']}")
    
    print("配置参数加载测试完成")

def test_path_logic():
    """测试路径处理逻辑"""
    print("\n测试路径处理逻辑...")
    
    # 模拟latex2handwritten.py中的路径处理逻辑
    def test_output_path_logic(output_file, format="png", is_dir=False):
        """测试输出路径处理逻辑"""
        # 检查output_file是否是目录路径
        if is_dir or (not os.path.splitext(output_file)[1]):
            # 如果是目录或没有扩展名的路径（通常是GUI选择的文件夹输出）
            # 使用output_file作为目录路径
            dir_path = output_file
            # 使用默认的base_name
            base_name = "output"
            # 扩展名始终使用format参数
            ext = f".{format}"
        else:
            # 分离目录路径和文件名
            dir_path = os.path.dirname(output_file)
            file_name = os.path.basename(output_file)
            
            # 分离文件名和扩展名
            base_name, ext = os.path.splitext(file_name)
            
            # 如果没有扩展名，使用format参数作为默认扩展名
            if not ext:
                ext = f".{format}"
        
        # 重新组合完整路径
        page_file_name = f"{base_name}_page_1{ext}"
        page_output_file = os.path.join(dir_path, page_file_name)
        
        return page_output_file
    
    # 测试用例
    test_cases = [
        # (output_file, format, is_dir, expected_result)
        ("test_output", "png", True, os.path.join("test_output", "output_page_1.png")),
        ("test_output", "png", False, os.path.join("test_output", "output_page_1.png")),  # 无扩展名
        ("test_output/output.png", "png", False, os.path.join("test_output", "output_page_1.png")),
        ("C:/test/output", "jpg", False, os.path.join("C:/test/output", "output_page_1.jpg")),  # 绝对路径，无扩展名，视为目录
    ]
    
    for i, (output_file, format, is_dir, expected) in enumerate(test_cases):
        result = test_output_path_logic(output_file, format, is_dir)
        if result == expected:
            print(f"  测试用例 {i+1} 正确：{result}")
        else:
            print(f"  测试用例 {i+1} 错误：期望 {expected}，实际 {result}")
    
    print("路径处理逻辑测试完成")

if __name__ == "__main__":
    test_config_loading()
    test_path_logic()
    print("\n所有测试完成！")
