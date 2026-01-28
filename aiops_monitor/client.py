# -*- coding: utf-8 -*-
"""
API 客户端模块
"""

import json
import logging
import traceback as tb
from datetime import datetime
from typing import Optional, Dict, Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import MonitorConfig

logger = logging.getLogger(__name__)


class MonitorClient:
    """监控 API 客户端"""
    
    def __init__(self, config: MonitorConfig):
        self.config = config
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """创建 requests session 并配置重试"""
        session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=self.config.max_retries,
            backoff_factor=self.config.retry_delay,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # 设置默认 headers
        session.headers.update({
            'Content-Type': 'application/json',
            'X-API-Key': self.config.api_key,
            'User-Agent': f'aiops-monitor/0.1.0'
        })
        
        return session
    
    def send_log(
        self,
        level: str,
        message: str,
        traceback: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        发送日志到监控系统
        
        Args:
            level: 日志级别
            message: 日志消息
            traceback: 异常堆栈
            context: 额外上下文
            
        Returns:
            是否发送成功
        """
        if not self.config.enabled:
            return False
        
        try:
            url = f"{self.config.api_url}/logs"
            
            payload = {
                'level': level.lower(),
                'message': message,
                'timestamp': datetime.utcnow().isoformat(),
            }
            
            if traceback:
                payload['traceback'] = traceback
            
            if context:
                payload['context'] = context
            
            response = self.session.post(
                url,
                json=payload,
                timeout=self.config.timeout
            )
            
            if response.status_code == 200:
                return True
            else:
                logger.warning(
                    f"监控日志发送失败: {response.status_code} - {response.text}"
                )
                return False
                
        except Exception as e:
            logger.error(f"监控日志发送异常: {e}")
            return False
    
    def format_log_data(
        self,
        record: logging.LogRecord
    ) -> Dict[str, Any]:
        """
        格式化日志记录
        
        Args:
            record: logging.LogRecord 对象
            
        Returns:
            格式化后的日志数据
        """
        data = {
            'level': record.levelname.lower(),
            'message': record.getMessage(),
            'timestamp': datetime.utcnow().isoformat(),
            'context': {
                'logger': record.name,
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno,
                'thread': record.thread,
                'process': record.process,
            }
        }
        
        # 添加项目名称（如果配置了）
        if self.config.project_name:
            data['context']['project'] = self.config.project_name
        
        # 提取异常信息
        if record.exc_info:
            data['traceback'] = ''.join(
                tb.format_exception(*record.exc_info)
            )
        
        return data
    
    def close(self):
        """关闭 session"""
        if self.session:
            self.session.close()
