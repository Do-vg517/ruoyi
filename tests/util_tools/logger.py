# -*- coding:utf-8 -*-
# @Time : 2025/10/16 19:00:00
# @Author: 刘晶祖
# @File : logger.py
# @Description : 日志配置工具模块
# =========================

import os
import logging

def setup_logger(log_dir=None, log_file="test.log", level=logging.INFO):
    """
    配置Python标准日志 - 同时输出到控制台和文件
    
    Args:
        log_dir: 日志目录路径，默认为项目根目录下的logs目录
        log_file: 日志文件名
        level: 日志级别，默认为INFO
    """
    # 设置默认日志目录为项目根目录下的logs目录
    if log_dir is None:
        # 获取项目根目录
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        log_dir = os.path.join(parent_dir, "log")
    
    # 创建日志目录
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, log_file)

    # 创建logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # 清除已有的handler
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # 创建文件handler - 强制使用UTF-8编码
    file_handler = logging.FileHandler(log_path, encoding='utf-8', mode='w')
    file_handler.setLevel(level)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_formatter)

    # 创建控制台handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_formatter)

    # 添加handler到logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_logger():
    """
    获取配置好的logger实例
    """
    return logging.getLogger()

# 默认配置
setup_logger()