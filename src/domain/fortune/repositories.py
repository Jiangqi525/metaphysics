# src/domain/fortune/repositories.py
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from uuid import UUID
from src.domain.fortune.entities import FortuneAnalysis


class AlgorithmMetadata:
    """算法元数据模型"""

    def __init__(self,
                 algorithm_type: str,
                 version: str,
                 module_path: str,
                 description: str = "",
                 dependencies: list = None,
                 is_active: bool = True):
        self.algorithm_type = algorithm_type
        self.version = version
        self.module_path = module_path
        self.description = description
        self.dependencies = dependencies or []
        self.is_active = is_active

    def to_dict(self) -> Dict:
        return {
            "algorithm_type": self.algorithm_type,
            "version": self.version,
            "module_path": self.module_path,
            "description": self.description,
            "dependencies": self.dependencies,
            "is_active": self.is_active
        }


class FortuneAnalysisRepository(ABC):
    """命理分析存储库接口"""

    @abstractmethod
    def save(self, analysis: FortuneAnalysis) -> None:
        """保存命理分析结果"""
        pass

    @abstractmethod
    def find_by_id(self, analysis_id: UUID) -> Optional[FortuneAnalysis]:
        """根据ID查找命理分析结果"""
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: UUID) -> list[FortuneAnalysis]:
        """根据用户ID查找命理分析结果"""
        pass

    @abstractmethod
    def update(self, analysis: FortuneAnalysis) -> None:
        """更新命理分析结果"""
        pass

    @abstractmethod
    def delete(self, analysis_id: UUID) -> None:
        """删除命理分析结果"""
        pass


class AlgorithmRepository(ABC):
    """算法元数据存储库接口"""

    @abstractmethod
    def get_algorithm_metadata(self, algorithm_type: str, version: str = None) -> Optional[AlgorithmMetadata]:
        """获取指定类型和版本的算法元数据"""
        pass

    @abstractmethod
    def list_algorithms(self, algorithm_type: Optional[str] = None) -> list[AlgorithmMetadata]:
        """列出所有可用算法（可选按类型过滤）"""
        pass

    @abstractmethod
    def register_algorithm(self, metadata: AlgorithmMetadata) -> None:
        """注册新算法"""
        pass

    @abstractmethod
    def update_algorithm(self, metadata: AlgorithmMetadata) -> None:
        """更新算法元数据"""
        pass

    @abstractmethod
    def deactivate_algorithm(self, algorithm_type: str, version: str) -> None:
        """停用指定算法"""
        pass