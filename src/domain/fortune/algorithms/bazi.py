from typing import Dict, Any, Tuple, List
import datetime
import pytz
import ephem
import lunardate
import numpy as np
from collections import Counter
from src.config.loader import CONSTANTS

# # 天干地支映射
# HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
# EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
#
# # 五行属性映射
# WUXING_MAP = {
#     "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
#     "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水",
#     "寅": "木", "卯": "木", "巳": "火", "午": "火", "辰": "土",
#     "戌": "土", "丑": "土", "未": "土", "申": "金", "酉": "金",
#     "亥": "水", "子": "水"
# }
#
# # 五行生克关系
# WUXING_RELATIONS = {
#     "木": {"生": "火", "克": "土", "被生": "水", "被克": "金"},
#     "火": {"生": "土", "克": "金", "被生": "木", "被克": "水"},
#     "土": {"生": "金", "克": "水", "被生": "火", "被克": "木"},
#     "金": {"生": "水", "克": "木", "被生": "土", "被克": "火"},
#     "水": {"生": "木", "克": "火", "被生": "金", "被克": "土"}
# }
HEAVENLY_STEMS = CONSTANTS['HEAVENLY_STEMS']
EARTHLY_BRANCHES = CONSTANTS['EARTHLY_BRANCHES']
WUXING_MAP = CONSTANTS['WUXING_MAP']
WUXING_RELATIONS = CONSTANTS['WUXING_RELATIONS']
BRANCH_HIDDEN_STEMS = CONSTANTS['BRANCH_HIDDEN_STEMS']
TEN_GODS_MAP = CONSTANTS['TEN_GODS_MAP']
ZODIAC_MAP = CONSTANTS['ZODIAC_MAP']
MING_GONG_EXPLANATIONS = CONSTANTS['MING_GONG_EXPLANATIONS']
# # 地支藏干映射（本气+余气）
# BRANCH_HIDDEN_STEMS = {
#     "子": [("癸", 1.0)],
#     "丑": [("己", 0.6), ("癸", 0.25), ("辛", 0.15)],
#     "寅": [("甲", 0.7), ("丙", 0.2), ("戊", 0.1)],
#     "卯": [("乙", 1.0)],
#     "辰": [("戊", 0.6), ("乙", 0.25), ("癸", 0.15)],
#     "巳": [("丙", 0.7), ("庚", 0.2), ("戊", 0.1)],
#     "午": [("丁", 0.7), ("己", 0.3)],
#     "未": [("己", 0.6), ("丁", 0.25), ("乙", 0.15)],
#     "申": [("庚", 0.7), ("壬", 0.2), ("戊", 0.1)],
#     "酉": [("辛", 1.0)],
#     "戌": [("戊", 0.6), ("辛", 0.25), ("丁", 0.15)],
#     "亥": [("壬", 0.7), ("甲", 0.3)]
# }
#
# # 十神关系映射
# TEN_GODS_MAP = {
#     "比肩": ["甲甲", "乙乙", "丙丙", "丁丁", "戊戊", "己己", "庚庚", "辛辛", "壬壬", "癸癸"],
#     "劫财": ["甲乙", "乙甲", "丙丁", "丁丙", "戊己", "己戊", "庚辛", "辛庚", "壬癸", "癸壬"],
#     "食神": ["甲丙", "乙丁", "丙戊", "丁己", "戊庚", "己辛", "庚壬", "辛癸", "壬甲", "癸乙"],
#     "伤官": ["甲丁", "乙丙", "丙己", "丁戊", "戊辛", "己庚", "庚癸", "辛壬", "壬乙", "癸甲"],
#     "正财": ["甲己", "乙戊", "丙辛", "丁庚", "戊癸", "己壬", "庚乙", "辛甲", "壬丁", "癸丙"],
#     "偏财": ["甲戊", "乙己", "丙庚", "丁辛", "戊壬", "己癸", "庚甲", "辛乙", "壬丙", "癸丁"],
#     "正官": ["甲辛", "乙庚", "丙癸", "丁壬", "戊乙", "己甲", "庚丁", "辛丙", "壬己", "癸戊"],
#     "七杀": ["甲庚", "乙辛", "丙壬", "丁癸", "戊甲", "己乙", "庚丙", "辛丁", "壬戊", "癸己"],
#     "正印": ["甲癸", "乙壬", "丙乙", "丁甲", "戊丁", "己丙", "庚己", "辛戊", "壬辛", "癸庚"],
#     "偏印": ["甲壬", "乙癸", "丙甲", "丁乙", "戊丙", "己丁", "庚戊", "辛己", "壬庚", "癸辛"]
# }
#
# # 生肖映射
# ZODIAC_MAP = {
#     "子": "鼠", "丑": "牛", "寅": "虎", "卯": "兔",
#     "辰": "龙", "巳": "蛇", "午": "马", "未": "羊",
#     "申": "猴", "酉": "鸡", "戌": "狗", "亥": "猪"
# }
#
# # 命宫解释映射
# MING_GONG_EXPLANATIONS = {
#     "子": "智慧深远，善于谋略，性格内敛。代表先天的智慧和思考能力。",
#     "丑": "踏实稳重，耐力强，财富积累型。代表先天的稳定性和物质基础。",
#     "寅": "积极进取，行动力强，领导才能。代表先天的活力和领导力。",
#     "卯": "聪明敏锐，适应力强，善于交际。代表先天的适应性和社交能力。",
#     "辰": "胸怀宽广，包容性强，贵人运佳。代表先天的包容性和人脉资源。",
#     "巳": "思维缜密，洞察力强，适合研究。代表先天的洞察力和专注力。",
#     "午": "热情开朗，精力充沛，事业心强。代表先天的热情和事业驱动力。",
#     "未": "温和善良，责任心强，家庭观念重。代表先天的责任感和家庭观念。",
#     "申": "机智灵活，应变力强，多才多艺。代表先天的灵活性和创造力。",
#     "酉": "注重细节，完美主义，艺术天赋。代表先天的审美和艺术感知力。",
#     "戌": "忠诚可靠，正义感强，适合公职。代表先天的正直和忠诚品质。",
#     "亥": "感性敏锐，想象力丰富，适合创作。代表先天的直觉和想象力。"
# }


def get_solar_terms(year: int) -> Dict[str, datetime.datetime]:
    """计算指定年份的24节气时间（完整版）"""
    solar_terms = {}
    observer = ephem.Observer()
    observer.lat = '0'
    observer.lon = '0'
    observer.elevation = 0

    # 更精确的节气计算
    term_calculations = {
        "立春": lambda d: ephem.next_vernal_equinox(d),
        "雨水": lambda d: ephem.next_new_moon(ephem.next_vernal_equinox(d)),
        "惊蛰": lambda d: ephem.next_new_moon(ephem.next_vernal_equinox(d)) + 15,
        "春分": lambda d: ephem.next_vernal_equinox(d),
        "清明": lambda d: ephem.next_new_moon(ephem.next_vernal_equinox(d)) + 30,
        "谷雨": lambda d: ephem.next_new_moon(ephem.next_vernal_equinox(d)) + 45,
        "立夏": lambda d: ephem.next_summer_solstice(d),
        "小满": lambda d: ephem.next_new_moon(ephem.next_summer_solstice(d)) + 15,
        "芒种": lambda d: ephem.next_new_moon(ephem.next_summer_solstice(d)) + 30,
        "夏至": lambda d: ephem.next_summer_solstice(d),
        "小暑": lambda d: ephem.next_new_moon(ephem.next_summer_solstice(d)) + 45,
        "大暑": lambda d: ephem.next_new_moon(ephem.next_summer_solstice(d)) + 60,
        "立秋": lambda d: ephem.next_autumnal_equinox(d),
        "处暑": lambda d: ephem.next_new_moon(ephem.next_autumnal_equinox(d)) + 15,
        "白露": lambda d: ephem.next_new_moon(ephem.next_autumnal_equinox(d)) + 30,
        "秋分": lambda d: ephem.next_autumnal_equinox(d),
        "寒露": lambda d: ephem.next_new_moon(ephem.next_autumnal_equinox(d)) + 45,
        "霜降": lambda d: ephem.next_new_moon(ephem.next_autumnal_equinox(d)) + 60,
        "立冬": lambda d: ephem.next_winter_solstice(d),
        "小雪": lambda d: ephem.next_new_moon(ephem.next_winter_solstice(d)) + 15,
        "大雪": lambda d: ephem.next_new_moon(ephem.next_winter_solstice(d)) + 30,
        "冬至": lambda d: ephem.next_winter_solstice(d),
        "小寒": lambda d: ephem.next_new_moon(ephem.next_winter_solstice(d)) + 45,
        "大寒": lambda d: ephem.next_new_moon(ephem.next_winter_solstice(d)) + 60
    }

    # 计算每个节气的时间
    for term, calc_func in term_calculations.items():
        try:
            # 设置初始日期为前一年的12月1日
            base_date = f"{year - 1}/12/1"
            term_date = calc_func(base_date)
            observer.date = term_date
            solar_terms[term] = observer.date.datetime()
        except Exception as e:
            print(f"计算节气{term}失败: {str(e)}")
            # 使用近似值作为后备方案
            month = (list(term_calculations.keys()).index(term) // 2 + 1)
            solar_terms[term] = datetime.datetime(year, month, 1) + datetime.timedelta(days=15)

    return solar_terms


def calculate_year_pillar(birth_datetime: datetime.datetime) -> Tuple[str, str]:
    """计算年柱（精确节气版）"""
    year = birth_datetime.year
    month = birth_datetime.month
    day = birth_datetime.day

    # 计算立春时间
    solar_terms = get_solar_terms(year)
    spring_date = solar_terms.get("立春", datetime.datetime(year, 2, 4))

    # 判断是否在立春之前
    if birth_datetime < spring_date:
        year -= 1

    # 计算年柱索引（1900年为庚子年）
    base_year = 1900
    base_index = 36  # 庚子在60甲子中的索引

    # 计算年柱索引
    year_index = (year - base_year + base_index) % 60
    stem_index = year_index % 10
    branch_index = year_index % 12

    return HEAVENLY_STEMS[stem_index], EARTHLY_BRANCHES[branch_index]


def calculate_month_pillar(birth_datetime: datetime.datetime, year_stem: str) -> Tuple[str, str]:
    """计算月柱（精确节气版）"""
    # 获取所有节气
    solar_terms = get_solar_terms(birth_datetime.year)

    # 定义节气顺序
    term_order = [
        "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
        "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
        "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
        "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
    ]

    # 找到出生日期前的最后一个节气
    last_term = None
    for term in term_order:
        term_date = solar_terms.get(term)
        if term_date and term_date < birth_datetime:
            last_term = term
        else:
            break

    # 确定月支（根据节气）
    if last_term:
        term_index = term_order.index(last_term)
        month_branch_index = (term_index // 2 + 2) % 12
    else:
        # 默认处理
        month_branch_index = (birth_datetime.month - 1) % 12

    # 五虎遁口诀确定月干
    stem_starts = {
        "甲": "丙", "己": "丙",  # 甲己之年丙作首
        "乙": "戊", "庚": "戊",  # 乙庚之岁戊为头
        "丙": "庚", "辛": "庚",  # 丙辛必定寻庚起
        "丁": "壬", "壬": "壬",  # 丁壬壬位顺行流
        "戊": "甲", "癸": "甲"  # 戊癸何方发，甲寅之上好追求
    }

    start_stem = stem_starts.get(year_stem, "丙")
    start_index = HEAVENLY_STEMS.index(start_stem)
    stem_index = (start_index + month_branch_index) % 10

    return HEAVENLY_STEMS[stem_index], EARTHLY_BRANCHES[month_branch_index]


def calculate_day_pillar(birth_datetime: datetime.datetime) -> Tuple[str, str]:
    """计算日柱（精确天文历法版）"""
    # 计算儒略日
    jd = ephem.julian_date(birth_datetime)

    # 公式计算日柱（基于1900年1月1日为甲戌日）
    base_jd = ephem.julian_date(datetime.datetime(1900, 1, 1))
    days_diff = jd - base_jd
    day_index = int(days_diff) % 60

    stem_index = day_index % 10
    branch_index = day_index % 12

    return HEAVENLY_STEMS[stem_index], EARTHLY_BRANCHES[branch_index]


def calculate_hour_pillar(birth_datetime: datetime.datetime, day_stem: str) -> Tuple[str, str]:
    """计算时柱（完整处理时区）"""
    # 转换到UTC时间
    utc_datetime = birth_datetime.astimezone(pytz.utc)
    hour = utc_datetime.hour
    minute = utc_datetime.minute

    # 处理晚子时（23:00-0:00）
    is_late_zi = hour == 23 or (hour == 0 and minute == 0)

    # 确定时辰地支
    if is_late_zi:
        branch_index = 0  # 子时
        # 晚子时使用次日日干
        next_day = birth_datetime + datetime.timedelta(days=1)
        next_day_stem, _ = calculate_day_pillar(next_day)
        day_stem = next_day_stem
    else:
        branch_index = ((hour + 1) // 2) % 12

    hour_branch = EARTHLY_BRANCHES[branch_index]

    # 五鼠遁口诀确定时干
    stem_starts = {
        "甲": "甲", "己": "甲",  # 甲己还加甲
        "乙": "丙", "庚": "丙",  # 乙庚丙作初
        "丙": "戊", "辛": "戊",  # 丙辛从戊起
        "丁": "庚", "壬": "庚",  # 丁壬庚子居
        "戊": "壬", "癸": "壬"  # 戊癸何方发，壬子是真途
    }

    start_stem = stem_starts.get(day_stem, "甲")
    start_index = HEAVENLY_STEMS.index(start_stem)
    stem_index = (start_index + branch_index) % 10

    return HEAVENLY_STEMS[stem_index], hour_branch


def calculate_ming_gong(birth_datetime: datetime.datetime) -> str:
    """
    计算命宫（完整版）

    命宫计算步骤：
    1. 将农历月份转换为地支序号（按逆数月份规则）
    2. 将出生时辰转换为地支序号
    3. 使用公式计算命宫地支序号：ming_index = (month_index + hour_index) % 12
    4. 将地支序号转换为地支字符

    逆数月份规则：
    正月→子(0), 二月→亥(11), 三月→戌(10), 四月→酉(9)
    五月→申(8), 六月→未(7), 七月→午(6), 八月→巳(5)
    九月→辰(4), 十月→卯(3), 十一月→寅(2), 十二月→丑(1)
    """
    try:
        # 获取农历日期
        lunar_date = lunardate.LunarDate.fromSolarDate(
            birth_datetime.year,
            birth_datetime.month,
            birth_datetime.day
        )
        lunar_month = lunar_date.month

        # 转换农历月份为地支序号（逆数月份规则）
        month_mapping = {
            1: 0,  # 正月 → 子(0)
            2: 11,  # 二月 → 亥(11)
            3: 10,  # 三月 → 戌(10)
            4: 9,  # 四月 → 酉(9)
            5: 8,  # 五月 → 申(8)
            6: 7,  # 六月 → 未(7)
            7: 6,  # 七月 → 午(6)
            8: 5,  # 八月 → 巳(5)
            9: 4,  # 九月 → 辰(4)
            10: 3,  # 十月 → 卯(3)
            11: 2,  # 十一月 → 寅(2)
            12: 1  # 十二月 → 丑(1)
        }

        # 处理闰月（闰月按当月计算）
        if lunar_date.leap:
            lunar_month = lunar_month  # 闰月按当月处理

        month_index = month_mapping.get(lunar_month, 0)

        # 转换出生时辰为地支序号
        hour = birth_datetime.hour
        hour_mapping = {
            23: 0, 0: 0,  # 子时 (23-1)
            1: 1, 2: 1,  # 丑时 (1-3)
            3: 2, 4: 2,  # 寅时 (3-5)
            5: 3, 6: 3,  # 卯时 (5-7)
            7: 4, 8: 4,  # 辰时 (7-9)
            9: 5, 10: 5,  # 巳时 (9-11)
            11: 6, 12: 6,  # 午时 (11-13)
            13: 7, 14: 7,  # 未时 (13-15)
            15: 8, 16: 8,  # 申时 (15-17)
            17: 9, 18: 9,  # 酉时 (17-19)
            19: 10, 20: 10,  # 戌时 (19-21)
            21: 11, 22: 11  # 亥时 (21-23)
        }
        hour_index = hour_mapping.get(hour, 0)

        # 计算命宫地支序号
        ming_index = (month_index + hour_index) % 12

        return EARTHLY_BRANCHES[ming_index]

    except Exception as e:
        # 计算失败时返回默认值
        print(f"命宫计算错误: {str(e)}")
        return "子"  # 默认返回子


def analyze_wuxing(bazi: Dict[str, Any]) -> Dict[str, Any]:
    """分析五行属性和平衡（包含藏干）"""
    wuxing = {"木": 0.0, "火": 0.0, "土": 0.0, "金": 0.0, "水": 0.0}

    # 统计四柱中的五行
    for i in range(4):
        stem = bazi["heavenly_stems"][i]
        branch = bazi["earthly_branches"][i]

        # 天干五行
        stem_element = WUXING_MAP.get(stem, "")
        if stem_element:
            wuxing[stem_element] += 1.0

        # 地支五行（含藏干）
        hidden_stems = BRANCH_HIDDEN_STEMS.get(branch, [])
        for stem_char, weight in hidden_stems:
            element = WUXING_MAP.get(stem_char, "")
            if element:
                wuxing[element] += weight

    # 日主（日干）属性
    day_stem = bazi["heavenly_stems"][2]
    day_element = WUXING_MAP.get(day_stem, "")

    # 计算五行平衡
    total = sum(wuxing.values())
    if total > 0:
        for element in wuxing:
            wuxing[element] = round(wuxing[element] / total, 2)

    # 找出强五行和弱五行
    strong_elements = [e for e, v in wuxing.items() if v > 0.25]
    weak_elements = [e for e, v in wuxing.items() if v < 0.15]

    # 生成五行建议
    recommendation = generate_recommendation(wuxing, day_element)

    return {
        "main_elements": wuxing,
        "strong_elements": strong_elements,
        "weak_elements": weak_elements,
        "recommendation": recommendation,
        "day_element": day_element
    }


def analyze_ten_gods(bazi: Dict[str, Any]) -> Dict[str, List[str]]:
    """分析十神关系"""
    day_stem = bazi["heavenly_stems"][2]
    ten_gods = []

    for i in range(4):
        stem = bazi["heavenly_stems"][i]
        god = None

        for god_name, combinations in TEN_GODS_MAP.items():
            if f"{day_stem}{stem}" in combinations:
                god = god_name
                break

        ten_gods.append(god if god else "未知")

    return {"ten_gods": ten_gods}


def generate_recommendation(wuxing: Dict[str, float], day_element: str) -> str:
    """生成五行平衡建议（考虑生克关系）"""
    if not day_element or day_element not in WUXING_RELATIONS:
        return "无法分析日主属性"

    # 获取日主的生克关系
    relations = WUXING_RELATIONS[day_element]

    # 计算日主强弱
    day_strength = wuxing.get(day_element, 0.0)

    # 计算生我者（印星）的力量
    strengthen_key = relations["被生"]
    strengthen_value = wuxing.get(strengthen_key, 0.0)

    # 计算我生者（食伤）的力量
    weaken_key = relations["生"]
    weaken_value = wuxing.get(weaken_key, 0.0)

    # 计算克我者（官杀）的力量
    suppress_key = relations["被克"]
    suppress_value = wuxing.get(suppress_key, 0.0)

    # 生成建议
    recommendations = []

    # 日主弱且生我者弱
    if day_strength < 0.2 and strengthen_value < 0.15:
        rec = f"日主{day_element}弱，且{strengthen_key}（生{day_element}者）弱，"
        rec += f"建议加强{strengthen_key}元素："
        rec += {
            "木": "接触自然，佩戴绿色饰品，东方发展",
            "火": "参与社交，穿戴红色衣物，南方发展",
            "土": "亲近大地，使用黄色物品，中部地区发展",
            "金": "佩戴金属饰品，白色衣物，西方发展",
            "水": "多接触水，黑色/蓝色衣物，北方发展"
        }.get(strengthen_key, "")
        recommendations.append(rec)

    # 日主强且我生者弱
    elif day_strength > 0.3 and weaken_value < 0.15:
        rec = f"日主{day_element}过旺，且{weaken_key}（{day_element}生者）弱，"
        rec += f"建议加强{weaken_key}元素："
        rec += {
            "木": "培养创造力，接触艺术，东方发展",
            "火": "参与公益活动，分享知识，南方发展",
            "土": "从事教育工作，分享经验，中部发展",
            "金": "培养逻辑思维，学习新技能，西方发展",
            "水": "参与社交活动，拓展人脉，北方发展"
        }.get(weaken_key, "")
        recommendations.append(rec)

    # 日主弱且克我者强
    elif day_strength < 0.2 and suppress_value > 0.25:
        rec = f"日主{day_element}弱，且{suppress_key}（克{day_element}者）强，"
        rec += f"建议加强{strengthen_key}元素以化解克制："
        rec += {
            "木": "多接触植物，佩戴绿色饰品",
            "火": "多晒太阳，穿戴红色衣物",
            "土": "亲近大地，使用黄色物品",
            "金": "佩戴金属饰品，白色衣物",
            "水": "多喝水，黑色/蓝色衣物"
        }.get(strengthen_key, "")
        recommendations.append(rec)

    # 平衡建议
    if not recommendations:
        strongest = max(wuxing, key=wuxing.get)
        weakest = min(wuxing, key=wuxing.get)

        if wuxing[strongest] > 0.3:
            rec = f"您的{strongest}元素过旺，建议适当抑制："
            rec += {
                "木": "接触金属元素，培养耐心，避免冲动",
                "火": "接触水元素，保持冷静，避免急躁",
                "土": "接触木元素，保持灵活，避免固执",
                "金": "接触火元素，避免固执，培养变通",
                "水": "接触土元素，保持务实，避免空想"
            }.get(strongest, "")
            recommendations.append(rec)

        if wuxing[weakest] < 0.1:
            rec = f"您的{weakest}元素过弱，建议加强："
            rec += {
                "木": "多接触植物，佩戴绿色饰品，东方发展",
                "火": "多晒太阳，穿戴红色衣物，南方发展",
                "土": "亲近大地，使用黄色物品，中部发展",
                "金": "佩戴金属饰品，白色衣物，西方发展",
                "水": "多喝水，黑色/蓝色衣物，北方发展"
            }.get(weakest, "")
            recommendations.append(rec)

    if not recommendations:
        return "您的五行较为平衡，运势顺畅，保持当前生活方式即可。"

    return " ".join(recommendations)


def find_nearest_jieqi(birth_datetime: datetime.datetime, direction: str) -> datetime.datetime:
    """找到最近的换月节气（向前或向后）"""
    # 定义12个换月节气（节）
    jieqi_names = ["立春", "惊蛰", "清明", "立夏", "芒种", "小暑",
                   "立秋", "白露", "寒露", "立冬", "大雪", "小寒"]

    # 获取出生年份及前后一年的节气
    years = [birth_datetime.year - 1, birth_datetime.year, birth_datetime.year + 1]
    all_jieqi = {}

    for year in years:
        solar_terms = get_solar_terms(year)
        for name, dt in solar_terms.items():
            if name in jieqi_names:
                all_jieqi[dt] = name

    # 按时间排序所有节气
    sorted_jieqi = sorted(all_jieqi.items(), key=lambda x: x[0])

    # 根据方向找到最近的节气
    if direction == "forward":
        # 顺行：找下一个节气
        for dt, name in sorted_jieqi:
            if dt > birth_datetime:
                return dt
    else:  # backward
        # 逆行：找上一个节气
        prev_jieqi = None
        for dt, name in sorted_jieqi:
            if dt < birth_datetime:
                prev_jieqi = dt
            else:
                break
        return prev_jieqi if prev_jieqi else sorted_jieqi[0][0]

    # 如果没找到，返回默认值
    return birth_datetime + datetime.timedelta(days=30)


def calculate_start_years(birth_datetime: datetime.datetime, direction: str) -> float:
    """精确计算起运年数"""
    # 根据方向找到最近的换月节气
    nearest_jieqi = find_nearest_jieqi(birth_datetime, direction)

    # 计算时间差
    if direction == "forward":
        delta = nearest_jieqi - birth_datetime
    else:  # backward
        delta = birth_datetime - nearest_jieqi

    # 计算总秒数并转换为天数
    total_seconds = delta.total_seconds()
    days = total_seconds / (24 * 3600)

    # 三天折合一岁，一天折合四个月
    years = days / 3

    # 精确到小数点后两位（表示年数）
    return round(years, 2)


def calculate_bazi(birth_data: Dict[str, Any]) -> Dict[str, Any]:
    """计算八字命盘（完整版）"""
    try:
        # 解析出生日期
        birth_datetime_str = birth_data.get("birth_datetime")
        timezone_str = birth_data.get("timezone", "Asia/Shanghai")

        # 创建带时区的datetime对象
        naive_datetime = datetime.datetime.fromisoformat(birth_datetime_str)
        timezone = pytz.timezone(timezone_str)
        birth_datetime = timezone.localize(naive_datetime)

        # 计算年柱
        year_stem, year_branch = calculate_year_pillar(birth_datetime)

        # 计算月柱
        month_stem, month_branch = calculate_month_pillar(birth_datetime, year_stem)

        # 计算日柱
        day_stem, day_branch = calculate_day_pillar(birth_datetime)

        # 计算时柱
        hour_stem, hour_branch = calculate_hour_pillar(birth_datetime, day_stem)

        # 组合八字
        bazi = {
            "heavenly_stems": [year_stem, month_stem, day_stem, hour_stem],
            "earthly_branches": [year_branch, month_branch, day_branch, hour_branch],
            "birth_datetime": birth_datetime.isoformat()
        }

        # 五行分析
        wuxing_analysis = analyze_wuxing(bazi)

        # 十神分析
        ten_gods_analysis = analyze_ten_gods(bazi)

        # 生肖计算
        zodiac = ZODIAC_MAP.get(year_branch, "未知")

        # 命宫计算
        ming_gong = calculate_ming_gong(birth_datetime)
        ming_gong_explanation = MING_GONG_EXPLANATIONS.get(ming_gong, "")

        # 大运起运时间计算（完整版）
        gender = birth_data.get("gender", "male")
        yang_year = year_stem in ["甲", "丙", "戊", "庚", "壬"]

        if gender == "male":
            start_direction = "顺行" if yang_year else "逆行"
        else:
            start_direction = "逆行" if yang_year else "顺行"

        # 计算起运年数
        direction = "forward" if start_direction == "顺行" else "backward"
        start_years = calculate_start_years(birth_datetime, direction)

        return {
            **bazi,
            **wuxing_analysis,
            **ten_gods_analysis,
            "zodiac": zodiac,
            "ming_gong": ming_gong,
            "ming_gong_explanation": ming_gong_explanation,
            "start_direction": start_direction,
            "start_years": start_years
        }

    except Exception as e:
        raise ValueError(f"八字计算失败: {str(e)}")


# 示例用法
if __name__ == "__main__":
    birth_data = {
        "birth_datetime": "1990-05-15T10:30:00",
        "timezone": "Asia/Shanghai",
        "gender": "male"
    }

    print("开始计算八字命盘...")
    result = calculate_bazi(birth_data)

    print("\n八字命盘:")
    print(f"年柱: {result['heavenly_stems'][0]}{result['earthly_branches'][0]}")
    print(f"月柱: {result['heavenly_stems'][1]}{result['earthly_branches'][1]}")
    print(f"日柱: {result['heavenly_stems'][2]}{result['earthly_branches'][2]}")
    print(f"时柱: {result['heavenly_stems'][3]}{result['earthly_branches'][3]}")

    print("\n命理分析:")
    print(f"生肖: {result['zodiac']}")
    print(f"命宫: {result['ming_gong']} - {result['ming_gong_explanation']}")
    print(f"大运: {result['start_direction']}, 约{result['start_years']}岁起运")

    print("\n十神关系:")
    print(f"年柱: {result['ten_gods'][0]}")
    print(f"月柱: {result['ten_gods'][1]}")
    print(f"日柱: {result['ten_gods'][2]}")
    print(f"时柱: {result['ten_gods'][3]}")

    print("\n五行分布:")
    for element, value in result['main_elements'].items():
        print(f"{element}: {value:.2f}")

    print(f"\n强五行: {', '.join(result['strong_elements'])}")
    print(f"弱五行: {', '.join(result['weak_elements'])}")

    print("\n运势建议:")
    print(result['recommendation'])

    print("\n八字计算完成！")
