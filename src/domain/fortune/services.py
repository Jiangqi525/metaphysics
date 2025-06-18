# src/domain/fortune/services.py
import importlib
from typing import Dict, Any, Optional, Callable, List
from uuid import UUID
from src.domain.core.exceptions import AlgorithmNotFoundError, ConfigNotFoundError
from src.domain.fortune.repositories import AlgorithmRepository, FortuneAnalysisRepository, AlgorithmMetadata
from src.domain.fortune.entities import FortuneAnalysis, BirthData, BaziResult, ZiweiResult
from src.infrastructure.utils.dynamic_config import DynamicConfigService
import logging

logger = logging.getLogger(__name__)


class FortuneCalculationService:
    """命理计算服务 - 处理各种命理算法的动态加载和执行"""

    def __init__(self,
                 algorithm_repository: AlgorithmRepository,
                 dynamic_config_service: DynamicConfigService):
        self.algorithm_repo = algorithm_repository
        self.dynamic_config_service = dynamic_config_service
        self.loaded_algorithms: Dict[str, Any] = {}  # 缓存已加载的算法模块
        self.algorithm_type_config_map = {
            "bazi": "fortune.bazi.default_version",
            "ziwei": "fortune.ziwei.default_version",
            "face": "fortune.face.default_version",
            "palm": "fortune.palm.default_version"
        }

    def _get_default_version(self, algorithm_type: str) -> str:
        """获取指定算法类型的默认版本"""
        try:
            config_key = self.algorithm_type_config_map.get(algorithm_type)
            if not config_key:
                raise ConfigNotFoundError(f"Config key not found for algorithm type: {algorithm_type}")

            config = self.dynamic_config_service.get_config(config_key)
            version = config.get("version", "v1.0")
            logger.debug(f"Using default {algorithm_type} algorithm version from config: {version}")
            return version
        except ConfigNotFoundError:
            version = "v1.0"
            logger.warning(f"Default {algorithm_type} algorithm version config not found, "
                           f"falling back to hardcoded: {version}")
            return version

    def _load_algorithm(self, algorithm_type: str, version: str) -> Callable:
        """加载并返回指定类型和版本的算法模块"""
        algorithm_key = f"{algorithm_type}_{version}"

        if algorithm_key not in self.loaded_algorithms:
            # 从算法仓库获取元数据
            metadata = self.algorithm_repo.get_algorithm_metadata(algorithm_type, version)
            if not metadata:
                raise AlgorithmNotFoundError(algorithm_type, version)

            # 动态加载算法模块
            try:
                module = importlib.import_module(metadata.module_path)
                if not hasattr(module, 'calculate'):
                    raise AlgorithmNotFoundError(
                        f"Algorithm module {metadata.module_path} missing 'calculate' function")

                self.loaded_algorithms[algorithm_key] = module
                logger.info(f"Loaded {algorithm_type} algorithm version {version} "
                            f"from module: {metadata.module_path}")
            except ImportError as e:
                logger.error(f"Failed to import algorithm module: {metadata.module_path}, Error: {e}")
                raise AlgorithmNotFoundError(algorithm_type, version)

        return self.loaded_algorithms[algorithm_key]

    def calculate_bazi(self, birth_data: BirthData, version: Optional[str] = None) -> BaziResult:
        """计算八字命理分析结果"""
        version = version or self._get_default_version("bazi")
        algorithm = self._load_algorithm("bazi", version)

        try:
            result_data = algorithm.calculate(birth_data.to_dict())
            return BaziResult(**result_data)
        except Exception as e:
            logger.error(f"Error calculating Bazi: {e}")
            raise AlgorithmNotFoundError(f"Error in Bazi calculation: {e}")

    def calculate_ziwei(self,
                        birth_data: BirthData,
                        location_data: Dict[str, float],
                        version: Optional[str] = None) -> ZiweiResult:
        """计算紫微斗数命理分析结果"""
        version = version or self._get_default_version("ziwei")
        algorithm = self._load_algorithm("ziwei", version)

        try:
            input_data = {
                "birth_data": birth_data.to_dict(),
                "location_data": location_data
            }
            result_data = algorithm.calculate(input_data)
            return ZiweiResult(**result_data)
        except Exception as e:
            logger.error(f"Error calculating Ziwei: {e}")
            raise AlgorithmNotFoundError(f"Error in Ziwei calculation: {e}")

    def calculate_fortune_analysis(self,
                                   user_id: UUID,
                                   birth_data: BirthData,
                                   location_data: Optional[Dict[str, float]] = None,
                                   analysis_types: Optional[List[str]] = None) -> FortuneAnalysis:
        """执行完整的命理分析流程，包括八字、紫微斗数等多种算法"""
        analysis_types = analysis_types or ["bazi", "ziwei"]

        analysis = FortuneAnalysis(
            user_id=user_id,
            analysis_type="_".join(analysis_types),
            birth_data=birth_data
        )

        if "bazi" in analysis_types:
            bazi_result = self.calculate_bazi(birth_data)
            analysis.update_bazi_result(bazi_result)
            analysis.wuxing_analysis = bazi_result.main_elements

        if "ziwei" in analysis_types and location_data:
            ziwei_result = self.calculate_ziwei(birth_data, location_data)
            analysis.update_ziwei_result(ziwei_result)

        # 计算幸运珠宝
        if analysis.wuxing_analysis:
            analysis.lucky_jewelry_ids = self._calculate_lucky_jewelry(analysis.wuxing_analysis)

        return analysis

    def _calculate_lucky_jewelry(self, wuxing_analysis: Dict[str, float]) -> List[int]:
        """根据五行分析结果计算推荐的幸运珠宝ID"""
        # 简化实现，实际应用中会更复杂
        lucky_jewelry = []

        # 假设每种五行对应特定的珠宝类别
        element_jewelry_map = {
            "wood": [101, 102, 103],  # 木属性珠宝
            "fire": [201, 202, 203],  # 火属性珠宝
            "earth": [301, 302, 303],  # 土属性珠宝
            "metal": [401, 402, 403],  # 金属性珠宝
            "water": [501, 502, 503]  # 水属性珠宝
        }

        # 找出最弱的五行属性
        weak_elements = sorted(wuxing_analysis.items(), key=lambda x: x[1])[:2]

        for element, _ in weak_elements:
            if element in element_jewelry_map:
                lucky_jewelry.extend(element_jewelry_map[element])

        return list(set(lucky_jewelry))  # 去重