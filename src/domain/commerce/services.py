# src/domain/commerce/services.py
import decimal
from typing import List, Optional
from uuid import UUID
from src.domain.commerce.entities import Order, Promotion
from src.domain.commerce.repositories import OrderRepository, PromotionRepository
from src.domain.core.value_objects import Money
from src.domain.jewelry.entities import Jewelry
from src.domain.jewelry.repositories import JewelryRepository


class CommerceService:
    def __init__(self,
                 order_repository: OrderRepository,
                 promotion_repository: PromotionRepository,
                 jewelry_repository: JewelryRepository):
        self.order_repo = order_repository
        self.promotion_repo = promotion_repository
        self.jewelry_repo = jewelry_repository

    def create_order(self, user_id: UUID, jewelry_ids: List[UUID]) -> Order:
        """创建订单"""
        total_price = Money(decimal.Decimal(0))
        for jewelry_id in jewelry_ids:
            jewelry = self.jewelry_repo.find_by_id(jewelry_id)
            if jewelry:
                total_price += jewelry.price

        order = Order(user_id=user_id, jewelry_ids=jewelry_ids, total_price=total_price)
        self.order_repo.save(order)
        return order

    def get_order_by_id(self, order_id: UUID) -> Optional[Order]:
        """根据ID获取订单"""
        return self.order_repo.find_by_id(order_id)

    def get_orders_by_user_id(self, user_id: UUID) -> List[Order]:
        """根据用户ID获取订单"""
        return self.order_repo.find_by_user_id(user_id)

    def pay_order(self, order_id: UUID) -> Order:
        """支付订单"""
        order = self.get_order_by_id(order_id)
        if not order:
            raise ValueError("Order not found.")
        order.pay_order()
        self.order_repo.update(order)
        return order

    def ship_order(self, order_id: UUID) -> Order:
        """发货订单"""
        order = self.get_order_by_id(order_id)
        if not order:
            raise ValueError("Order not found.")
        order.ship_order()
        self.order_repo.update(order)
        return order

    def complete_order(self, order_id: UUID) -> Order:
        """完成订单"""
        order = self.get_order_by_id(order_id)
        if not order:
            raise ValueError("Order not found.")
        order.complete_order()
        self.order_repo.update(order)
        return order

    def cancel_order(self, order_id: UUID) -> Order:
        """取消订单"""
        order = self.get_order_by_id(order_id)
        if not order:
            raise ValueError("Order not found.")
        order.cancel_order()
        self.order_repo.update(order)
        return order

    def create_promotion(self,
                         promotion_name: str,
                         discount_rate: float,
                         start_time: str,
                         end_time: str,
                         applicable_jewelry_categories: List[int]) -> Promotion:
        """创建促销活动"""
        promotion = Promotion(promotion_name=promotion_name,
                              discount_rate=discount_rate,
                              start_time=start_time,
                              end_time=end_time,
                              applicable_jewelry_categories=applicable_jewelry_categories)
        self.promotion_repo.save(promotion)
        return promotion

    def get_active_promotions(self) -> List[Promotion]:
        """获取所有活跃的促销活动"""
        return self.promotion_repo.find_all_active()

    def deactivate_promotion(self, promotion_id: UUID) -> Promotion:
        """停用促销活动"""
        promotion = self.promotion_repo.find_by_id(promotion_id)
        if not promotion:
            raise ValueError("Promotion not found.")
        promotion.deactivate_promotion()
        self.promotion_repo.update(promotion)
        return promotion

    def activate_promotion(self, promotion_id: UUID) -> Promotion:
        """启用促销活动"""
        promotion = self.promotion_repo.find_by_id(promotion_id)
        if not promotion:
            raise ValueError("Promotion not found.")
        promotion.activate_promotion()
        self.promotion_repo.update(promotion)
        return promotion
