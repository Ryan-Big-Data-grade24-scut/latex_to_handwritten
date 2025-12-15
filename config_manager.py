#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块

功能：
1. 加载和保存配置文件
2. 支持多个预设配置
3. 提供默认配置
4. 支持配置验证
"""

import json
import os

class ConfigManager:
    """
    配置管理器
    """
    
    def __init__(self, config_file="config.json"):
        """
        初始化配置管理器
        
        Args:
            config_file (str): 配置文件路径
        """
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        """
        加载配置文件，如果文件不存在则创建默认配置
        
        Returns:
            dict: 配置字典
        """
        default_config = {
            "default": {
                "font": "IndieFlower-Regular",
                "resolution": 200,
                "randomness": 0.05,
                "a4": False,
                "markdown": False,
                "random_fonts": False,
                "mixed_rendering": False,
                "process_latex_markers": False,
                "max_chars": 50,
                "max_score": 15
            },
            "presets": {
                "all_enabled": {
                    "font": "IndieFlower-Regular",
                    "resolution": 200,
                    "randomness": 0.05,
                    "a4": True,
                    "markdown": True,
                    "random_fonts": True,
                    "mixed_rendering": True,
                    "process_latex_markers": True,
                    "max_chars": 50,
                    "max_score": 15
                }
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                
                # 合并默认配置和加载的配置
                default_config.update(loaded_config)
                return default_config
            except Exception as e:
                print(f"Error loading config file: {e}")
                return default_config
        else:
            # 保存默认配置
            self._save_config(default_config)
            return default_config
    
    def _save_config(self, config):
        """
        保存配置到文件
        
        Args:
            config (dict): 配置字典
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config file: {e}")
            return False
    
    def get_default_config(self):
        """
        获取默认配置
        
        Returns:
            dict: 默认配置
        """
        return self.config.get("default", {})
    
    def get_preset(self, preset_name):
        """
        获取预设配置
        
        Args:
            preset_name (str): 预设名称
            
        Returns:
            dict: 预设配置，如果不存在返回默认配置
        """
        return self.config.get("presets", {}).get(preset_name, self.get_default_config())
    
    def get_all_presets(self):
        """
        获取所有预设名称
        
        Returns:
            list: 预设名称列表
        """
        return list(self.config.get("presets", {}).keys())
    
    def save_preset(self, preset_name, preset_config):
        """
        保存预设配置
        
        Args:
            preset_name (str): 预设名称
            preset_config (dict): 预设配置
            
        Returns:
            bool: 是否保存成功
        """
        if "presets" not in self.config:
            self.config["presets"] = {}
        
        self.config["presets"][preset_name] = preset_config
        return self._save_config(self.config)
    
    def delete_preset(self, preset_name):
        """
        删除预设配置
        
        Args:
            preset_name (str): 预设名称
            
        Returns:
            bool: 是否删除成功
        """
        if "presets" in self.config and preset_name in self.config["presets"]:
            del self.config["presets"][preset_name]
            return self._save_config(self.config)
        return False
    
    def update_default_config(self, config):
        """
        更新默认配置
        
        Args:
            config (dict): 配置字典
            
        Returns:
            bool: 是否更新成功
        """
        self.config["default"].update(config)
        return self._save_config(self.config)

# 创建全局配置管理器实例
config_manager = ConfigManager()

# 便捷函数
def get_default_config():
    """
    获取默认配置
    
    Returns:
        dict: 默认配置
    """
    return config_manager.get_default_config()

def get_preset(preset_name):
    """
    获取预设配置
    
    Args:
        preset_name (str): 预设名称
        
    Returns:
        dict: 预设配置
    """
    return config_manager.get_preset(preset_name)

def get_all_presets():
    """
    获取所有预设名称
    
    Returns:
        list: 预设名称列表
    """
    return config_manager.get_all_presets()

def save_preset(preset_name, preset_config):
    """
    保存预设配置
    
    Args:
        preset_name (str): 预设名称
        preset_config (dict): 预设配置
        
    Returns:
        bool: 是否保存成功
    """
    return config_manager.save_preset(preset_name, preset_config)

def update_default_config(config):
    """
    更新默认配置
    
    Args:
        config (dict): 配置字典
        
    Returns:
        bool: 是否更新成功
    """
    return config_manager.update_default_config(config)