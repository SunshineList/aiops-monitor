# AI-Ops Monitor SDK

[![PyPI version](https://badge.fury.io/py/aiops-monitor.svg)](https://badge.fury.io/py/aiops-monitor)
[![Python](https://img.shields.io/pypi/pyversions/aiops-monitor.svg)](https://pypi.org/project/aiops-monitor/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🚀 **AI 驱动的日志监控与自动修复 SDK**

自动捕获应用错误，AI 分析根因并生成修复方案，让运维更智能！

## ✨ 特性

- 🎯 **零侵入集成** - 3 行代码接入监控
- ⚡ **异步上报** - 不影响应用性能
- 🤖 **AI 分析** - 自动分析错误根因
- 🔧 **自动修复** - AI 生成修复代码
- 📊 **可视化面板** - 实时查看错误趋势
- 🔔 **智能告警** - Telegram 通知
- 🌐 **多框架支持** - Django / Flask / FastAPI

## 📦 安装

```bash
pip install aiops-monitor

# Django 项目
pip install aiops-monitor[django]

# Flask 项目
pip install aiops-monitor[flask]

# FastAPI 项目
pip install aiops-monitor[fastapi]
```

## 🚀 快速开始

### Django 集成

```python
# settings.py

# 1. 添加到 INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'aiops_monitor.integrations.django',
]

# 2. 配置监控
AIOPS_MONITOR = {
    'api_url': 'http://your-monitor-server:8000/api/v1',
    'api_key': 'your-api-key',
    'project_name': 'My Django Project',
    'log_levels': ['ERROR', 'CRITICAL'],
    'async': True,
}
```

### Flask 集成

```python
from flask import Flask
from aiops_monitor import init_monitor

app = Flask(__name__)

# 初始化监控
init_monitor(
    app,
    api_url='http://your-monitor-server:8000/api/v1',
    api_key='your-api-key',
    project_name='My Flask App'
)

@app.route('/')
def index():
    # 错误会自动上报
    result = 1 / 0
    return 'Hello'
```

### FastAPI 集成

```python
from fastapi import FastAPI
from aiops_monitor import init_monitor

app = FastAPI()

init_monitor(
    app,
    api_url='http://your-monitor-server:8000/api/v1',
    api_key='your-api-key',
    project_name='My FastAPI App'
)

@app.get("/")
def read_root():
    # 错误会自动上报
    result = 1 / 0
    return {"Hello": "World"}
```

### 独立使用

```python
from aiops_monitor import MonitorClient, MonitorConfig
import logging

# 创建配置
config = MonitorConfig(
    api_url='http://your-monitor-server:8000/api/v1',
    api_key='your-api-key',
    project_name='My Script'
)

# 创建客户端
client = MonitorClient(config)

# 添加 handler
handler = client.get_handler(level=logging.ERROR)
logging.root.addHandler(handler)

# 使用
try:
    result = 1 / 0
except Exception:
    logging.error("发生错误", exc_info=True)  # 自动上报
```

## ⚙️ 配置选项

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `api_url` | str | ✅ | - | 监控服务地址 |
| `api_key` | str | ✅ | - | API 密钥 |
| `project_name` | str | ❌ | None | 项目名称 |
| `log_levels` | list | ❌ | `['ERROR', 'CRITICAL']` | 上报的日志级别 |
| `timeout` | int | ❌ | 5 | 请求超时时间（秒） |
| `async_mode` | bool | ❌ | True | 异步上报模式 |
| `max_retries` | int | ❌ | 3 | 最大重试次数 |
| `enabled` | bool | ❌ | True | 是否启用监控 |

## 🔍 工作流程

```
应用错误 → SDK 捕获 → 异步上报 → AI 分析
    ↓
修复代码 ← AI 生成 ← 根因定位
```

## 📊 监控面板

SDK 配合监控服务器使用，提供：

- 📈 **实时监控** - 错误统计和趋势分析
- 🔎 **智能聚合** - 相同错误自动归类
- 🤖 **AI 分析** - GPT-4 分析错误根因
- 💊 **自动修复** - 生成修复代码和 diff
- 📱 **Telegram 通知** - 实时告警推送

## 🛠️ 开发

```bash
# 克隆仓库
git clone https://github.com/SunshineList/aiops-monitor
cd aiops-monitor

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black aiops_monitor

# 类型检查
mypy aiops_monitor
```

## 📝 License

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

## 📮 联系

- Issues: https://github.com/SunshineList/aiops-monitor/issues

---

Made with ❤️ by Tuple
