"""
紫微斗数五行算法模块
包含五行局计算、纳音五行、星曜五行属性等核心算法
"""

from typing import List, Dict, Tuple, Optional
from lunarcalendar import Lunar
from src.config.loader import CONSTANTS

# 天干地支和五行映射
# HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
# EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
# WUXING_MAP = {
#     "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
#     "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水",
#     "寅": "木", "卯": "木", "巳": "火", "午": "火", "辰": "土",
#     "戌": "土", "丑": "土", "未": "土", "申": "金", "酉": "金",
#     "亥": "水", "子": "水"
# }

HEAVENLY_STEMS = CONSTANTS['HEAVENLY_STEMS']
EARTHLY_BRANCHES = CONSTANTS['EARTHLY_BRANCHES']
WUXING_MAP = CONSTANTS['WUXING_MAP']


class WuxingCalculator:
    """紫微斗数五行算法计算器"""

    def calculate_wuxing_bureau(self, lunar: Lunar, major_stars: Dict[str, List[str]]) -> str:
        """
        计算五行局
        1. 结合年干支纳音五行
        2. 考虑命宫主星五行属性
        """
        # 1. 计算年干支纳音五行
        year_stem = self._get_lunar_year_stem(lunar.year)
        year_branch = EARTHLY_BRANCHES[(lunar.year - 1900) % 12]
        nayin_wuxing = self._get_nayin_wuxing(year_stem, year_branch)

        # 2. 计算命宫主星五行
        life_palace = next(key for key in major_stars if "紫微" in major_stars[key])
        life_stars = major_stars[life_palace]
        star_wuxing = self._get_star_wuxing(life_stars)

        # 3. 综合确定五行局
        bureau_map = {
            "水": "水二局", "木": "木三局", "金": "金四局",
            "土": "土五局", "火": "火六局"
        }

        # 优先以纳音五行为主，命宫主星五行为辅
        main_wuxing = nayin_wuxing
        if not main_wuxing:
            main_wuxing = star_wuxing

        return bureau_map.get(main_wuxing, "土五局")

    def _get_lunar_year_stem(self, lunar_year: int) -> str:
        """获取农历年干"""
        stem_idx = (lunar_year - 1900) % 10
        return HEAVENLY_STEMS[stem_idx]

    def _get_nayin_wuxing(self, stem: str, branch: str) -> str:
        """获取年干支纳音五行（简化算法）"""
        stem_idx = HEAVENLY_STEMS.index(stem)
        branch_idx = EARTHLY_BRANCHES.index(branch)
        nayin_index = (stem_idx * 12 + branch_idx) % 5
        wuxing_list = ["金", "火", "木", "水", "土"]
        return wuxing_list[nayin_index]

    def _get_star_wuxing(self, stars: List[str]) -> str:
        """获取主星五行属性"""
        star_wuxing_map = {
            "紫微": "土", "天机": "木", "太阳": "火", "武曲": "金", "天同": "水", "廉贞": "火",
            "天府": "土", "太阴": "水", "贪狼": "木", "巨门": "土", "天相": "水", "天梁": "土",
            "七杀": "金", "破军": "水"
        }

        for star in stars:
            if star in star_wuxing_map:
                return star_wuxing_map[star]
        return ""

    def analyze_wuxing_relation(self, year_wuxing: str, bureau_wuxing: str) -> str:
        """分析流年五行与五行局的生克关系"""
        if not year_wuxing or not bureau_wuxing:
            return "平"

        wuxing_relations = CONSTANTS['WUXING_RELATIONS']

        if year_wuxing == bureau_wuxing:
            return "比和"  # 五行相同

        if wuxing_relations[year_wuxing]["生"] == bureau_wuxing:
            return "相生"  # 流年五行生五行局

        if wuxing_relations[year_wuxing]["克"] == bureau_wuxing:
            return "相克"  # 流年五行克五行局

        if wuxing_relations[bureau_wuxing]["生"] == year_wuxing:
            return "被生"  # 五行局生流年五行

        if wuxing_relations[bureau_wuxing]["克"] == year_wuxing:
            return "被克"  # 五行局克流年五行

        return "平"