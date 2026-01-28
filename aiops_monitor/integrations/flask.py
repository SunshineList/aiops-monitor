# -*- coding: utf-8 -*-
"""
Flask 集成模块
"""

import logging
from flask import Flask

from ..client import MonitorClient
from ..config import MonitorConfig
from ..handlers import MonitoringHandler


def setup_flask(app: Flask, client: MonitorClient, config: MonitorConfig):
    """
    设置 Flask 应用的监控
    
    Args:
        app: Flask 应用实例
        client: 监控客户端
        config: 监控配置
    """
    # 创建 handler
    handler = MonitoringHandler(
        client=client,
        config=config,
        level=getattr(logging, config.log_levels[0])
    )
    
    # 添加到 Flask logger
    app.logger.addHandler(handler)
    
    # 也添加到 root logger（捕获其他模块的日志）
    logging.root.addHandler(handler)
    
    # 关闭时清理
    @app.teardown_appcontext
    def cleanup(error=None):
        handler.close()
    
    return client
