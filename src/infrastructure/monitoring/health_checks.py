from flask import Blueprint, jsonify
from src.extensions import db, cache  # 假设db和cache是Flask扩展实例
import logging

logger = logging.getLogger(__name__)

health_bp = Blueprint('health', __name__)


@health_bp.route('/healthz', methods=)
def liveness_check():
    """
    Liveness probe: Checks if the application is running.
    A simple check for basic connectivity to critical dependencies.
    """
    try:
        # 检查数据库连接
        db.session.execute(db.text("SELECT 1"))
        # 检查缓存连接
        cache.get("health_check_key")  # 尝试从缓存读取
        logger.debug("Liveness check successful.")
        return jsonify({"status": "UP", "details": "Application is running and basic dependencies are reachable"}), 200
    except Exception as e:
        logger.error(f"Liveness check failed: {e}")
        return jsonify({"status": "DOWN", "error": str(e)}), 500


@health_bp.route('/readyz', methods=)
def readiness_check():
    """
    Readiness probe: Checks if the application is ready to serve traffic.
    More comprehensive check including resource initialization.
    """
    try:
        # 检查数据库连接和连接池状态
        db.session.execute(db.text("SELECT 1"))
        # 检查缓存连接和可用性
        cache.set("ready_check_key", "ok", timeout=1)  # 尝试写入和读取
        if cache.get("ready_check_key") != "ok":
            raise ConnectionError("Cache is not fully ready.")

        # 检查核心算法模型是否已加载或可访问
        # 例如：从动态配置服务中尝试获取一个关键配置，确保服务已初始化并能访问配置
        # from src.infrastructure.utils.dynamic_config import dynamic_config_service
        # dynamic_config_service.get_config("some_critical_algorithm_param")

        logger.debug("Readiness check successful.")
        return jsonify({"status": "READY", "details": "Application is ready to serve traffic"}), 200
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return jsonify({"status": "NOT_READY", "error": str(e)}), 503
