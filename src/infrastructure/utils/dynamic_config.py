import json
from sqlalchemy.orm import Session
from src.infrastructure.persistence.orm.system_config import SystemConfig
from src.domain.core.exceptions import ConfigNotFoundError
from src.infrastructure.utils.cache_manager import CacheManager  # 引入缓存管理器
import logging

logger = logging.getLogger(__name__)


class DynamicConfigService:
    def __init__(self, db_session_factory, cache_manager: CacheManager):
        self.db_session_factory = db_session_factory
        self.cache_manager = cache_manager
        self.config_cache_key_prefix = "dynamic_config:"

    def get_config(self, key):
        cache_key = self.config_cache_key_prefix + key
        # 尝试从缓存获取
        cached_value = self.cache_manager.get(cache_key)
        if cached_value is not None:
            logger.debug(f"Config '{key}' retrieved from cache.")
            return cached_value

        # 缓存未命中，从数据库查询
        with self.db_session_factory() as session:
            config = session.query(SystemConfig).filter_by(config_key=key).first()
            if not config:
                logger.warning(f"Config '{key}' not found in database.")
                raise ConfigNotFoundError(f"Config {key} not found")

            # 解析并缓存
            value = self._parse_config(config)
            # 设置合理的缓存过期时间，或通过事件驱动进行失效
            self.cache_manager.set(cache_key, value, ttl=300)  # 默认缓存5分钟
            logger.info(f"Config '{key}' loaded from DB and cached.")
            return value

    def update_config(self, key, new_value, config_type, description=None):
        with self.db_session_factory() as session:
            config = session.query(SystemConfig).filter_by(config_key=key).first()
            if not config:
                config = SystemConfig(config_key=key)
                session.add(config)

            config.config_value = str(new_value)
            config.config_type = config_type
            config.description = description
            session.commit()

            # 缓存失效：当配置更新时，立即从缓存中移除旧值
            self.cache_manager.delete(self.config_cache_key_prefix + key)
            logger.info(f"Config '{key}' updated in DB and cache invalidated.")

    def _parse_config(self, config):
        if config.config_type == 'json':
            return json.loads(config.config_value)
        elif config.config_type == 'int':
            return int(config.config_value)
        elif config.config_type == 'float':
            return float(config.config_value)
        elif config.config_type == 'boolean':
            return config.config_value.lower() == 'true'
        return config.config_value
