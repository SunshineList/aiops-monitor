# -*- coding: utf-8 -*-
"""
日志处理器模块
"""

import logging
import threading
from queue import Queue, Empty
from typing import Optional

from .client import MonitorClient
from .config import MonitorConfig


class MonitoringHandler(logging.Handler):
    """
    监控系统日志处理器
    异步发送日志到监控系统
    """
    
    def __init__(
        self,
        client: Optional[MonitorClient] = None,
        config: Optional[MonitorConfig] = None,
        level: int = logging.ERROR
    ):
        super().__init__(level)
        self.client = client
        self.config = config
        self.enabled = config.enabled if config else False
        
        # 异步队列
        if config and config.async_mode:
            self.queue = Queue(maxsize=1000)
            self.worker_thread = threading.Thread(
                target=self._worker,
                daemon=True,
                name='MonitorWorker'
            )
            self.worker_thread.start()
        else:
            self.queue = None
            self.worker_thread = None
    
    def emit(self, record: logging.LogRecord):
        """
        处理日志记录
        
        Args:
            record: 日志记录对象
        """
        if not self.config or not self.client:
            return

        try:
            # 检查是否启用
            if not self.config.enabled:
                return
            
            # 检查日志级别
            if record.levelname not in self.config.log_levels:
                return
            
            # 自定义过滤器
            if self.config.filter_func and not self.config.filter_func(record):
                return
            
            # 忽略特定模式
            if self._should_ignore(record):
                return
            
            # 格式化日志数据
            log_data = self.client.format_log_data(record)
            
            # 异步或同步发送
            if self.config.async_mode and self.queue:
                try:
                    self.queue.put_nowait(log_data)
                except:
                    # 队列满，丢弃日志
                    pass
            else:
                self._send_log(log_data)
                
        except Exception:
            self.handleError(record)
    
    def _should_ignore(self, record: logging.LogRecord) -> bool:
        """检查是否应该忽略该日志"""
        message = record.getMessage()
        for pattern in self.config.ignore_patterns:
            if pattern in message:
                return True
        return False
    
    def _worker(self):
        """后台工作线程，异步发送日志"""
        while True:
            try:
                log_data = self.queue.get(timeout=1.0)
                self._send_log(log_data)
                self.queue.task_done()
            except Empty:
                continue
            except Exception as e:
                logging.error(f"监控 worker 异常: {e}")
    
    def _send_log(self, log_data: dict):
        """发送日志"""
        try:
            self.client.send_log(
                level=log_data['level'],
                message=log_data['message'],
                traceback=log_data.get('traceback'),
                context=log_data.get('context')
            )
        except Exception as e:
            logging.error(f"发送监控日志失败: {e}")
    
    def close(self):
        """关闭处理器"""
        if self.queue and self.worker_thread:
            # 等待队列清空
            self.queue.join()
        
        if self.client:
            self.client.close()
        
        super().close()
