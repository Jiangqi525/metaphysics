# src/config/loader.py
import os
import yaml
from typing import Dict, List, Any

def load_constants() -> Dict[str, Any]:
    """加载YAML配置文件中的常量"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'constants.yaml')
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"错误: 配置文件 {config_path} 未找到")
        return {}
    except yaml.YAMLError as e:
        print(f"错误: 解析YAML文件失败: {e}")
        return {}

# 全局常量对象
CONSTANTS = load_constants()