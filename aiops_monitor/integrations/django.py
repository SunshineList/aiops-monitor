# -*- coding: utf-8 -*-
"""
Django 集成模块
"""

from django.apps import AppConfig
from django.conf import settings
import logging

from ..client import MonitorClient
from ..config import MonitorConfig
from ..handlers import MonitoringHandler


class AIOpsMonitorConfig(AppConfig):
    """Django App 配置"""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aiops_monitor.integrations.django'
    verbose_name = 'AI-Ops Monitor'
    
    def ready(self):
        """应用启动时初始化监控"""
        # 从 settings 读取配置
        monitor_config = getattr(settings, 'AIOPS_MONITOR', {})
        
        if not monitor_config:
            return
        
        try:
            # 创建配置对象
            config = MonitorConfig.from_dict(monitor_config)
            
            # 创建客户端
            client = MonitorClient(config)
            
            # 创建并注册 handler
            handler = MonitoringHandler(
                client=client,
                config=config,
                level=getattr(logging, config.log_levels[0])
            )
            
            # 添加到 root logger
            logging.root.addHandler(handler)
            
            print(f"✓ AI-Ops Monitor 已启用: {config.project_name or 'Unknown'}")
            
        except Exception as e:
            print(f"✗ AI-Ops Monitor 初始化失败: {e}")


# 默认配置
default_app_config = 'aiops_monitor.integrations.django.AIOpsMonitorConfig'
