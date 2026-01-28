"""
Django 使用示例
"""

# settings.py 配置

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 添加监控
    'aiops_monitor.integrations.django',
    
    # 你的应用
    'myapp',
]

# 监控配置
AIOPS_MONITOR = {
    'api_url': 'http://localhost:8000/api/v1',
    'api_key': 'your-api-key-here',
    'project_name': 'Django Example Project',
    'log_levels': ['ERROR', 'CRITICAL'],
    'async_mode': True,
    'timeout': 5,
}

# views.py - 触发错误示例

from django.http import JsonResponse
from django.views import View
import logging

logger = logging.getLogger(__name__)


class TestErrorView(View):
    """测试错误上报"""
    
    def get(self, request):
        try:
            # 故意触发错误
            result = 1 / 0
        except Exception as e:
            # 日志会自动上报到监控系统
            logger.error(f"计算错误: {e}", exc_info=True)
            return JsonResponse({
                'error': '计算失败',
                'message': '错误已上报到监控系统'
            }, status=500)
        
        return JsonResponse({'result': result})


class DatabaseErrorView(View):
    """测试数据库错误"""
    
    def get(self, request):
        from myapp.models import User
        
        try:
            # 触发数据库错误
            user = User.objects.get(id=99999)
        except User.DoesNotExist as e:
            logger.error(f"用户不存在: {e}", exc_info=True)
            return JsonResponse({
                'error': '用户不存在',
                'message': '错误已上报'
            }, status=404)
