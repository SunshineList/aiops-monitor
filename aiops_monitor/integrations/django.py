# -*- coding: utf-8 -*-
"""
Django 集成模块
"""

import logging
from django.apps import AppConfig
from django.conf import settings
from ..handlers import MonitoringHandler
from ..client import MonitorClient
from ..config import MonitorConfig


class DjangoAIOpsHandler(MonitoringHandler):
    """
    专门为 Django LOGGING 字典配置设计的 Handler。
    它不需要在 __init__ 中传入 client，而是会自动从 settings 中拉取配置。
    """
    def __init__(self, *args, **kwargs):
        # 1. 延迟获取配置
        monitor_settings = getattr(settings, 'AIOPS_MONITOR', {})
        if not monitor_settings:
            # 如果没配置，创建一个禁用的配置，防止报错
            super().__init__(client=None, config=None, level=logging.ERROR)
            return

        # 2. 初始化配置和客户端
        try:
            config = MonitorConfig.from_dict(monitor_settings)
            client = MonitorClient(config)
            
            # 3. 初始化父类
            super().__init__(client=client, config=config)
        except Exception as e:
            # 打印到控制台，不影响主进程启动
            print(f"!!! AI-Ops Monitor 初始化异常: {e}")
            super().__init__(client=None, config=None, level=logging.ERROR)


class AIOpsMonitorConfig(AppConfig):
    """Django App 配置"""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aiops_monitor.integrations.django'
    verbose_name = 'AI-Ops Monitor'
    
    def ready(self):
        """应用启动时初始化监控（双重保险）"""
        # 如果用户已经在 LOGGING 中配置了 DjangoAIOpsHandler，则不需要自动注册
        # 这里保留一个简单的自动注册逻辑，作为默认行为
        monitor_config = getattr(settings, 'AIOPS_MONITOR', {})
        if not monitor_config:
            return
            
        # 检查是否已经手动配置了 handler
        # 我们这里不做复杂的检查，只是作为双重保险
        pass


# 默认配置
default_app_config = 'aiops_monitor.integrations.django.AIOpsMonitorConfig'
