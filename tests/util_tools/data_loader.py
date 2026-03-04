import os
import yaml


class DataLoader:
    """数据加载工具类"""
    
    @staticmethod
    def load_yaml(file_path, key=None):
        """
        加载YAML文件数据
        :param file_path: 相对于项目根目录的路径，例如 "tests/data/login_data.yaml"
        :param key: YAML文件中的键名，如果提供，则返回对应键的数据
        """
        # 获取项目根目录（假设此文件在 tests/util_tools/data_loader.py）
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        abs_path = os.path.join(base_dir, file_path)
        
        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if key:
                    key_data = data.get(key, [])
                    print(f"DEBUG: Loaded data for key '{key}' from {file_path}: {key_data}")
                    return key_data
                return data
        except Exception as e:
            print(f"Error loading YAML file {abs_path}: {e}")
            return []