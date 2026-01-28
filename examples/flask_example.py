"""
Flask 使用示例
"""

from flask import Flask, jsonify
from aiops_monitor import init_monitor
import logging

app = Flask(__name__)

# 初始化监控
init_monitor(
    app,
    api_url='http://localhost:8000/api/v1',
    api_key='your-api-key-here',
    project_name='Flask Example App'
)

logger = logging.getLogger(__name__)


@app.route('/')
def index():
    return jsonify({'message': 'Hello from Flask!'})


@app.route('/error')
def test_error():
    """测试错误上报"""
    try:
        result = 1 / 0
    except Exception as e:
        logger.error(f"计算错误: {e}", exc_info=True)
        return jsonify({
            'error': '计算失败',
            'message': '错误已上报到监控系统'
        }), 500


@app.route('/db-error')
def test_db_error():
    """测试数据库错误"""
    try:
        # 模拟数据库错误
        from sqlalchemy import create_engine
        engine = create_engine('postgresql://invalid:invalid@localhost/invalid')
        engine.connect()
    except Exception as e:
        logger.error(f"数据库连接失败: {e}", exc_info=True)
        return jsonify({
            'error': '数据库错误',
            'message': '错误已上报'
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
