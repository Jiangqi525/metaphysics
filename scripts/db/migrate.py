from alembic.config import Config
from alembic import command
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# 导入所有ORM模型文件，确保Alembic能发现所有表
# 必须导入所有Base的子类，否则Alembic无法识别这些表
import src.infrastructure.persistence.orm.base
import src.infrastructure.persistence.orm.user_models
import src.infrastructure.persistence.orm.fate_models
import src.infrastructure.persistence.orm.jewelry_models
import src.infrastructure.persistence.orm.healing_models
import src.infrastructure.persistence.orm.ecommerce_models
import src.infrastructure.persistence.orm.social_models

# ... 导入所有其他ORM模型文件

logger = logging.getLogger(__name__)


def run_migrations():
    """
    执行数据库迁移，将数据库升级到最新版本。
    """
    alembic_cfg = Config("alembic.ini")

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        logger.error("DATABASE_URL environment variable not set.")
        raise ValueError("DATABASE_URL is required for database migrations.")

    alembic_cfg.set_main_option("sqlalchemy.url", database_url)

    try:
        # 获取当前数据库版本
        current_rev = command.current(alembic_cfg)
        # 获取最新版本（head）
        head_rev = command.heads(alembic_cfg)

        if current_rev != head_rev:
            logger.info(f"Upgrading database from {current_rev if current_rev else 'initial'} to {head_rev}")
            command.upgrade(alembic_cfg, "head")
            logger.info("Database migration completed successfully.")

            # 记录迁移日志（可以写入到单独的迁移日志表或外部日志系统）
            # log_migration_event(current_rev, head_rev) # 假设有这个函数
        else:
            logger.info("Database is already at the latest revision.")
    except Exception as e:
        logger.critical(f"Database migration failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    run_migrations()
