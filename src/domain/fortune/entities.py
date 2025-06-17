# src/domain/fortune/entities.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from uuid import UUID
from src.domain.core.entities import AggregateRoot
from src.domain.core.value_objects import BirthData


@dataclass
class BaziResult:
    heavenly_stems: List[str] = field(default_factory=list)  # 天干
    earthly_branches: List[str] = field(default_factory=list)  # 地支
    main_elements: Dict[str, float] = field(default_factory=dict)  # 主要五行
    strong_elements: List[str] = field(default_factory=list)  # 强五行
    weak_elements: List[str] = field(default_factory=list)  # 弱五行
    recommendation: str = ""  # 推荐建议

    def to_dict(self) -> Dict:
        return {
            "heavenly_stems": self.heavenly_stems,
            "earthly_branches": self.earthly_branches,
            "main_elements": self.main_elements,
            "strong_elements": self.strong_elements,
            "weak_elements": self.weak_elements,
            "recommendation": self.recommendation
        }


@dataclass
class ZiweiResult:
    life_palace: str = ""  # 命宫
    major_stars: List[str] = field(default_factory=list)  # 主星
    star_interactions: List[Dict[str, str]] = field(default_factory=list)  # 星曜互动
    fortune_trend: str = ""  # 运势趋势
    recommendation: str = ""  # 推荐建议

    def to_dict(self) -> Dict:
        return {
            "life_palace": self.life_palace,
            "major_stars": self.major_stars,
            "star_interactions": self.star_interactions,
            "fortune_trend": self.fortune_trend,
            "recommendation": self.recommendation
        }


@dataclass
class FortuneAnalysis(AggregateRoot):
    user_id: UUID
    analysis_type: str  # 分析类型(bazi, ziwei, face, palm)
    birth_data: BirthData
    bazi_result: BaziResult = field(default_factory=BaziResult)
    ziwei_result: ZiweiResult = field(default_factory=ZiweiResult)
    wuxing_analysis: Dict[str, float] = field(default_factory=dict)
    emotion_trend: Dict[str, float] = field(default_factory=dict)
    lucky_jewelry_ids: List[int] = field(default_factory=list)
    confidence_score: float = 0.0
    created_at: str = field(default_factory=lambda: str(datetime.datetime.now()))

    def update_bazi_result(self, result: BaziResult) -> None:
        self.bazi_result = result
        self.updated_at = str(datetime.datetime.now())

    def update_ziwei_result(self, result: ZiweiResult) -> None:
        self.ziwei_result = result
        self.updated_at = str(datetime.datetime.now())

    def add_lucky_jewelry(self, jewelry_id: int) -> None:
        if jewelry_id not in self.lucky_jewelry_ids:
            self.lucky_jewelry_ids.append(jewelry_id)
            self.updated_at = str(datetime.datetime.now())
