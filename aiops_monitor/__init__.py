# -*- coding: utf-8 -*-
"""
AI-Ops Monitor SDK
智能日志监控与自动修复 Python SDK
"""

__version__ = "0.1.2"
__author__ = "Tuple"

from .client import MonitorClient
from .config import MonitorConfig
from .handlers import MonitoringHandler

# 便捷初始化函数
def init_monitor(app=None, **kwargs):
    """
    初始化监控
    
    Args:
        app: 应用实例（Flask/FastAPI/Django 等）
        **kwargs: 配置参数
        
    Examples:
        # Flask
        >>> from flask import Flask
        >>> app = Flask(__name__)
        >>> init_monitor(app, api_url='...', api_key='...')
        
        # FastAPI
        >>> from fastapi import FastAPI
        >>> app = FastAPI()
        >>> init_monitor(app, api_url='...', api_key='...')
        
        # 独立使用
        >>> init_monitor(api_url='...', api_key='...')
    """
    config = MonitorConfig(**kwargs)
    client = MonitorClient(config)
    
    if app is None:
        # 独立使用，添加到 root logger
        import logging
        handler = MonitoringHandler(client, config)
        logging.root.addHandler(handler)
        return client
    
    # 检测框架类型并集成
    app_type = type(app).__module__
    
    if 'flask' in app_type.lower():
        from .integrations.flask import setup_flask
        return setup_flask(app, client, config)
    elif 'fastapi' in app_type.lower() or 'starlette' in app_type.lower():
        from .integrations.fastapi import setup_fastapi
        return setup_fastapi(app, client, config)
    else:
        raise ValueError(f"Unsupported framework: {app_type}")

__all__ = [
    'MonitorClient',
    'MonitorConfig', 
    'MonitoringHandler',
    'init_monitor',
]
