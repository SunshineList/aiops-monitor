"""
FastAPI 使用示例
"""

from fastapi import FastAPI, HTTPException
from aiops_monitor import init_monitor
import logging

app = FastAPI(title="FastAPI Example")

# 初始化监控
init_monitor(
    app,
    api_url='http://localhost:8000/api/v1',
    api_key='your-api-key-here',
    project_name='FastAPI Example App'
)

logger = logging.getLogger(__name__)


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}


@app.get("/error")
def test_error():
    """测试错误上报"""
    try:
        result = 1 / 0
    except Exception as e:
        logger.error(f"计算错误: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="计算失败，错误已上报到监控系统"
        )


@app.get("/items/{item_id}")
def read_item(item_id: int):
    """测试参数错误"""
    try:
        if item_id > 100:
            raise ValueError(f"Item ID {item_id} 超出范围")
        return {"item_id": item_id, "name": f"Item {item_id}"}
    except ValueError as e:
        logger.error(f"参数错误: {e}", exc_info=True)
        raise HTTPException(status_code=400,  detail=str(e))


@app.get("/db-error")
async def test_db_error():
    """测试异步错误"""
    try:
        # 模拟异步数据库错误
        raise ConnectionError("数据库连接失败")
    except Exception as e:
        logger.error(f"数据库错误: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="数据库错误，已上报"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
