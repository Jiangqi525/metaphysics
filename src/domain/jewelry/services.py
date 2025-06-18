# src/domain/jewelry/services.py
from typing import List, Optional
from uuid import UUID
from src.domain.jewelry.entities import Jewelry, JewelryCategory
from src.domain.jewelry.repositories import JewelryRepository, JewelryCategoryRepository


class JewelryService:
    def __init__(self, jewelry_repository: JewelryRepository, category_repository: JewelryCategoryRepository):
        self.jewelry_repo = jewelry_repository
        self.category_repo = category_repository

    def create_jewelry(self, jewelry: Jewelry) -> Jewelry:
        """创建珠宝"""
        category = self.category_repo.find_by_id(jewelry.category_id)
        if not category:
            raise ValueError("Jewelry category not found")
        self.jewelry_repo.save(jewelry)
        return jewelry

    def get_jewelry_by_id(self, jewelry_id: UUID) -> Optional[Jewelry]:
        """根据ID获取珠宝"""
        return self.jewelry_repo.find_by_id(jewelry_id)

    def get_all_jewelry(self) -> List[Jewelry]:
        """获取所有珠宝"""
        return self.jewelry_repo.find_all()

    def update_jewelry(self, jewelry: Jewelry) -> Jewelry:
        """更新珠宝信息"""
        category = self.category_repo.find_by_id(jewelry.category_id)
        if not category:
            raise ValueError("Jewelry category not found")
        self.jewelry_repo.update(jewelry)
        return jewelry

    def delete_jewelry(self, jewelry_id: UUID) -> None:
        """删除珠宝信息"""
        self.jewelry_repo.delete(jewelry_id)


class JewelryCategoryService:
    def __init__(self, category_repository: JewelryCategoryRepository):
        self.category_repo = category_repository

    def create_category(self, category: JewelryCategory) -> JewelryCategory:
        """创建珠宝分类"""
        self.category_repo.save(category)
        return category

    def get_category_by_id(self, category_id: int) -> Optional[JewelryCategory]:
        """根据ID获取珠宝分类"""
        return self.category_repo.find_by_id(category_id)

    def get_all_categories(self) -> List[JewelryCategory]:
        """获取所有珠宝分类"""
        return self.category_repo.find_all()

    def update_category(self, category: JewelryCategory) -> JewelryCategory:
        """更新珠宝分类信息"""
        self.category_repo.update(category)
        return category

    def delete_category(self, category_id: int) -> None:
        """删除珠宝分类信息"""
        self.category_repo.delete(category_id)