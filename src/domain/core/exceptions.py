# src/domain/core/exceptions.py
class DomainException(Exception):
    """领域层基础异常"""
    pass

class BusinessRuleViolation(DomainException):
    """业务规则违反异常"""
    def __init__(self, message: str):
        super().__init__(f"Business rule violation: {message}")

class EntityNotFound(DomainException):
    """实体未找到异常"""
    def __init__(self, entity_type: str, entity_id: str):
        super().__init__(f"{entity_type} with id {entity_id} not found")

class AlgorithmNotFoundError(DomainException):
    """算法未找到异常"""
    def __init__(self, algorithm_name: str, version: str = None):
        version_info = f" version {version}" if version else ""
        super().__init__(f"Algorithm {algorithm_name}{version_info} not found")

class ConfigNotFoundError(DomainException):
    """配置未找到异常"""
    def __init__(self, config_key: str):
        super().__init__(f"Configuration with key {config_key} not found")