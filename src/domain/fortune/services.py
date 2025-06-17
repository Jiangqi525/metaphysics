import importlib
from src.domain.core.exceptions import AlgorithmNotFoundError, ConfigNotFoundError
from src.domain.fortune.repositories import AlgorithmRepository  # 假设AlgorithmRepository能获取算法元数据
from src.infrastructure.utils.dynamic_config import DynamicConfigService  # 引入动态配置服务
import logging

logger = logging.getLogger(__name__)


class FortuneCalculationService:
    def __init__(self, algorithm_repository: AlgorithmRepository, dynamic_config_service: DynamicConfigService):
        self.algorithm_repo = algorithm_repository
        self.dynamic_config_service = dynamic_config_service
        self.loaded_algorithms = {}  # 缓存已加载的算法模块

    def _load_algorithm_module(self, module_path):
        """动态加载算法模块并缓存"""
        if module_path not in self.loaded_algorithms:
            try:
                self.loaded_algorithms[module_path] = importlib.import_module(module_path)
                logger.info(f"Dynamically loaded algorithm module: {module_path}")
            except ImportError as e:
                logger.error(f"Failed to load algorithm module {module_path}: {e}")
                raise AlgorithmNotFoundError(f"Failed to load algorithm module {module_path}: {e}")
        return self.loaded_algorithms[module_path]

    def calculate_bazi(self, user_birth_data, version=None):
        """
        计算八字。
        如果未指定版本，则从动态配置中获取默认版本。
        """
        if version is None:
            # 从动态配置获取当前八字算法的默认版本
            try:
                default_bazi_version_config = self.dynamic_config_service.get_config("fortune.bazi.default_version")
                version = default_bazi_version_config.get("version", "v1.0")  # 默认值
                logger.debug(f"Using default Bazi algorithm version from config: {version}")
            except ConfigNotFoundError:
                version = "v1.0"  # 如果配置不存在，使用硬编码默认值
                logger.warning(f"Default Bazi algorithm version config not found, falling back to hardcoded: {version}")

        # 从算法仓库获取指定版本的算法元数据
        algorithm_metadata = self.algorithm_repo.get_algorithm_metadata("bazi", version)
        if not algorithm_metadata:
            raise AlgorithmNotFoundError(f"Bazi algorithm version {version} not found in repository.")

        # 动态加载算法模块并调用其计算方法
        module = self._load_algorithm_module(algorithm_metadata.module_path)

        # 假设算法模块中有一个名为 'calculate' 的函数
        if not hasattr(module, 'calculate'):
            raise AlgorithmNotFoundError(
                f"Algorithm module {algorithm_metadata.module_path} has no 'calculate' function.")

        return module.calculate(user_birth_data)

    # 其他玄学算法（如紫微斗数）也采用类似的版本管理方式
    def calculate_ziwei(self, user_birth_data, location_data, version=None):
        if version is None:
            try:
                default_ziwei_version_config = self.dynamic_config_service.get_config("fortune.ziwei.default_version")
                version = default_ziwei_version_config.get("version", "v1.0")
                logger.debug(f"Using default Ziwei algorithm version from config: {version}")
            except ConfigNotFoundError:
                version = "v1.0"
                logger.warning(
                    f"Default Ziwei algorithm version config not found, falling back to hardcoded: {version}")

        algorithm_metadata = self.algorithm_repo.get_algorithm_metadata("ziwei", version)
        if not algorithm_metadata:
            raise AlgorithmNotFoundError(f"Ziwei algorithm version {version} not found in repository.")

        module = self._load_algorithm_module(algorithm_metadata.module_path)
        if not hasattr(module, 'calculate'):
            raise AlgorithmNotFoundError(
                f"Algorithm module {algorithm_metadata.module_path} has no 'calculate' function.")

        return module.calculate(user_birth_data, location_data)
