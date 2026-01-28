# -*- coding: utf-8 -*-
"""
FastAPI 集成模块
"""

import logging
from fastapi import FastAPI

from ..client import MonitorClient
from ..config import MonitorConfig
from ..handlers import MonitoringHandler


def setup_fastapi(app: FastAPI, client: MonitorClient, config: MonitorConfig):
    """
    设置 FastAPI 应用的监控
    
    Args:
        app: FastAPI 应用实例
        client: 监控客户端
        config: 监控配置
    """
    # 创建 handler
    handler = MonitoringHandler(
        client=client,
        config=config,
        level=getattr(logging, config.log_levels[0])
    )
    
    # 添加到 root logger
    logging.root.addHandler(handler)
    
    # 启动和关闭事件
    @app.on_event("startup")
    async def startup():
        pass
    
    @app.on_event("shutdown")
    async def shutdown():
        handler.close()
    
    return client
