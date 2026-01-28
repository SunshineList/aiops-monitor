# -*- coding: utf-8 -*-
"""
配置管理模块
"""

from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class MonitorConfig:
    """监控配置类"""
    
    # 必需配置
    api_url: str
    api_key: str
    
    # 可选配置
    project_name: Optional[str] = None
    log_levels: List[str] = field(default_factory=lambda: ['ERROR', 'CRITICAL'])
    timeout: int = 5
    async_mode: bool = True
    
    # 重试配置
    max_retries: int = 3
    retry_delay: float = 1.0
    
    # 高级配置
    enabled: bool = True
    filter_func: Optional[callable] = None
    ignore_patterns: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """验证配置"""
        if not self.api_url:
            raise ValueError("api_url is required")
        if not self.api_key:
            raise ValueError("api_key is required")
        
        # 规范化 API URL
        self.api_url = self.api_url.rstrip('/')
        
        # 转换日志级别为大写
        self.log_levels = [level.upper() for level in self.log_levels]
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> 'MonitorConfig':
        """从字典创建配置"""
        return cls(**config_dict)
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'api_url': self.api_url,
            'api_key': self.api_key,
            'project_name': self.project_name,
            'log_levels': self.log_levels,
            'timeout': self.timeout,
            'async_mode': self.async_mode,
            'max_retries': self.max_retries,
            'retry_delay': self.retry_delay,
            'enabled': self.enabled,
        }
