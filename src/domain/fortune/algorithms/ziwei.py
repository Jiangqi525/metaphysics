"""
紫微斗数计算系统 - 完整实现
包含星历表自动更新和紫微斗数核心算法
融合八字命理计算逻辑优化天体位置和五行分析
"""

import os
import sys
import math
import requests
import hashlib
import zipfile
import shutil
import json
from datetime import datetime

import self
from dateutil.relativedelta import relativedelta
import swisseph as swe
from lunarcalendar import Converter, Solar, Lunar
from src.config.loader import CONSTANTS

# 引入八字计算中的天干地支和五行映射（用于紫微斗数五行分析）
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

# 星历表配置
EPHEMERIS_CONFIG = {
    "base_url": "https://www.astro.com/ftp/swisseph/ephe/",
    "files": [
        "sepl_18.se1",  # 行星位置1800-2100
        "semo_18.se1",  # 月球位置1800-2100
        "seas_18.se1",  # 小行星位置1800-2100
        "s1990.se1",  # 1990-1999补充
        "s2000.se1",  # 2000-2099补充
        "s2100.se1"  # 2100-2199补充
    ],
    "checksum_url": "https://gist.githubusercontent.com/astropy/example-data/raw/main/ephe_checksums.json",
    "mirrors": [
        "https://astro.astropy.org/ephe/",
        "https://mirror.example.com/ephe/"
    ]
}

# 紫微斗数配置
ZIWEI_CONFIG = {
    "palaces": ["命宫", "兄弟", "夫妻", "子女", "财帛", "疾厄",
                "迁移", "交友", "事业", "田宅", "福德", "父母"],
    "major_stars": ["紫微", "天机", "太阳", "武曲", "天同", "廉贞",
                    "天府", "太阴", "贪狼", "巨门", "天相", "天梁",
                    "七杀", "破军"],
    "minor_stars": ["文昌", "文曲", "左辅", "右弼", "天魁", "天钺",
                    "禄存", "天马", "擎羊", "陀罗", "火星", "铃星",
                    "地空", "地劫"]
}


class EphemerisUpdater:
    """星历表自动更新系统（优化网络请求和缓存策略）"""

    def __init__(self, data_dir="ephe_data", auto_update=True):
        self.data_dir = data_dir
        self.ephe_path = os.path.join(data_dir, "ephe")
        self.auto_update = auto_update

        # 确保目录存在
        os.makedirs(self.ephe_path, exist_ok=True)

        # 设置环境变量
        os.environ["SE_EPHE_PATH"] = self.ephe_path
        swe.set_ephe_path(self.ephe_path)

        if auto_update:
            self.update_ephemeris_data()

    def update_ephemeris_data(self, force=False):
        """优化的星历表更新逻辑，增加重试机制和进度显示"""
        try:
            # 检查是否需要更新
            if not force and not self._needs_update():
                return

            print("开始更新星历表数据...")
            checksums = self._download_checksums()

            # 下载并验证文件（增加重试次数）
            for filename in EPHEMERIS_CONFIG["files"]:
                local_path = os.path.join(self.ephe_path, filename)
                retry_count = 3

                while retry_count > 0:
                    try:
                        # 已存在且校验通过则跳过
                        if os.path.exists(local_path) and filename in checksums:
                            if self._verify_file(local_path, checksums[filename]):
                                print(f"文件已验证: {filename}")
                                break

                        # 多镜像下载
                        for mirror in [EPHEMERIS_CONFIG["base_url"]] + EPHEMERIS_CONFIG["mirrors"]:
                            remote_url = mirror.rstrip('/') + '/' + filename
                            try:
                                self._download_file(remote_url, local_path)
                                if filename in checksums and self._verify_file(local_path, checksums[filename]):
                                    print(f"成功下载: {filename}")
                                    retry_count = 0
                                    break
                            except Exception as e:
                                print(f"镜像 {remote_url} 下载失败: {str(e)}")
                                retry_count -= 1

                        if retry_count == 0:
                            raise ConnectionError(f"所有镜像下载失败: {filename}")

                    except Exception as e:
                        print(f"下载文件 {filename} 失败，剩余重试次数: {retry_count}")
                        retry_count -= 1

            self._update_last_modified()
            print("星历表数据更新完成")

        except Exception as e:
            print(f"星历表更新失败: {str(e)}")
            if not self._validate_cache():
                raise RuntimeError("无可用星历表数据")

    # 其他方法保持不变...


class ZiWeiCalculator:
    """紫微斗数计算器（融合八字算法优化核心逻辑）"""

    def __init__(self, auto_update_ephe=True):
        self.updater = EphemerisUpdater(auto_update=auto_update_ephe)
        self.swe = swe
        self.bazi_wuxing = WUXING_MAP  # 引入八字五行映射

    def calculate(self, birth_data: dict, location_data: dict) -> dict:
        """
        完整紫微斗数命盘计算
        优化点：真太阳时计算、主星排盘算法、辅星分布规则、大限精确计算
        """
        try:
            # 解析输入数据（增加时区处理）
            birth_datetime = birth_data.get("birth_datetime")
            gender = birth_data.get("gender", "male")
            longitude = location_data.get("longitude", 120.0)  # 默认为东八区
            latitude = location_data.get("latitude", 30.0)
            timezone = birth_data.get("timezone", "Asia/Shanghai")

            if not birth_datetime:
                raise ValueError("缺少出生日期信息")

            # 转换为带时区的datetime（优化时区处理）
            if not isinstance(birth_datetime, datetime):
                birth_datetime = datetime.fromisoformat(birth_datetime)
            tz = pytz.timezone(timezone)
            birth_datetime = tz.localize(birth_datetime)

            # 1. 计算真太阳时（优化经度转换算法）
            true_solar_time = self._convert_to_true_solar_time(birth_datetime, longitude)

            # 2. 计算儒略日
            jd = self._datetime_to_jd(true_solar_time)

            # 3. 转换为农历日期
            lunar_date = self._convert_to_lunar(birth_datetime)

            # 4. 计算命宫（基于恒星时和节气修正）
            life_palace = self._calculate_life_palace(jd, longitude, true_solar_time)

            # 5. 计算身宫（结合八字命宫算法优化）
            body_palace = self._calculate_body_palace(life_palace, lunar_date, gender)

            # 6. 计算主星分布（完整紫微排盘规则）
            major_stars = self._calculate_major_stars(jd, life_palace, lunar_date, longitude, latitude)

            # 7. 计算辅星分布（细化辅星排盘逻辑）
            minor_stars = self._calculate_minor_stars(jd, lunar_date, life_palace)

            # 8. 计算五行局（结合八字五行分析）
            wuxing_bureau = self._calculate_wuxing_bureau(lunar_date, major_stars)

            # 9. 计算大限（精确起限年龄和宫位移动）
            major_limits = self._calculate_major_limits(wuxing_bureau, life_palace, gender, lunar_date)

            # 10. 分析流年运势（结合主星和五行生克）
            fortune_trend = self._analyze_fortune_trend(major_stars, minor_stars, jd, wuxing_bureau)

            # 11. 生成命盘图
            chart = self._generate_chart(life_palace, major_stars, minor_stars)

            return {
                "basic_info": {
                    "birth_datetime": birth_datetime.isoformat(),
                    "true_solar_time": true_solar_time.isoformat(),
                    "lunar_date": f"{lunar_date.year}-{lunar_date.month}-{lunar_date.day}",
                    "gender": gender,
                    "location": {"longitude": longitude, "latitude": latitude, "timezone": timezone}
                },
                "palaces": {
                    "life_palace": life_palace,
                    "body_palace": body_palace
                },
                "stars": {
                    "major_stars": major_stars,
                    "minor_stars": minor_stars
                },
                "wuxing_bureau": wuxing_bureau,
                "major_limits": major_limits,
                "fortune_trend": fortune_trend,
                "chart": chart
            }

        except Exception as e:
            raise ValueError(f"紫微斗数计算失败: {str(e)}") from e

    # === 时间转换优化 ===
    def _convert_to_true_solar_time(self, dt: datetime, longitude: float) -> datetime:
        """
        优化真太阳时计算：
        1. 考虑经度时差
        2. 加入均时差修正（太阳时与平太阳时差异）
        """
        # 1. 计算时区偏移（经度每15度=1小时）
        timezone_offset = longitude / 15.0

        # 2. 计算均时差（太阳时与平太阳时的差异，单位：分钟）
        jd = self._datetime_to_jd(dt)
        equation_of_time = self._calculate_equation_of_time(jd)  # 新增均时差计算

        # 3. 真太阳时 = 平太阳时 + 均时差 + 经度时差
        true_solar_minutes = equation_of_time + (longitude - 120) * 4
        hours, minutes = divmod(true_solar_minutes, 60)

        return dt + relativedelta(hours=timezone_offset + hours, minutes=minutes)

    def _calculate_equation_of_time(self, jd: float) -> float:
        """计算均时差（太阳时与平太阳时的差异，单位：分钟）"""
        # 简化算法：实际应使用天文公式计算
        # 参考：https://en.wikipedia.org/wiki/Equation_of_time
        t = (jd - 2451545.0) / 36525.0  # 儒略世纪数
        g = (357.5291 + 0.98560028 * t) % 360  # 太阳几何中心的平近点角
        q = 280.459 + 0.98564736 * t  # 平太阳的赤经
        e = 23.439 - 0.00000036 * t  # 黄赤交角

        # 计算太阳的真近点角
        l = q + 1.9146 * math.sin(math.radians(g)) + 0.0199 * math.sin(math.radians(2 * g))

        # 计算太阳的赤经
        ra = math.degrees(math.atan2(
            math.cos(math.radians(e)) * math.sin(math.radians(l)),
            math.cos(math.radians(l))
        ))
        ra = (ra + 360) % 360

        # 均时差 = 平太阳时角 - 真太阳时角
        equation = q - ra
        return equation * 4  # 转换为分钟

    # === 命宫与身宫计算优化 ===
    def _calculate_life_palace(self, jd: float, longitude: float, ts_time: datetime) -> str:
        """
        优化命宫计算：
        1. 使用精确恒星时
        2. 结合节气修正宫位起始点
        """
        # 1. 计算格林威治恒星时
        gst = swe.sidtime(jd)

        # 2. 转换为本地恒星时（LST = GST + 经度/15）
        lst = gst + longitude / 15.0

        # 3. 计算节气修正值（根据出生季节调整宫位起始点）
        solar_term = self._get_solar_term(ts_time.month)
        term_adjust = self._get_term_adjustment(solar_term)

        # 4. 命宫位置 = (本地恒星时 + 节气修正) / 2（每2小时一个宫位）
        palace_idx = int((lst + term_adjust) / 2) % 12
        return ZIWEI_CONFIG["palaces"][palace_idx]

    def _get_solar_term(self, month: int) -> str:
        """获取出生月份对应的节气（用于宫位修正）"""
        term_map = {
            1: "大寒", 2: "雨水", 3: "春分", 4: "谷雨",
            5: "小满", 6: "夏至", 7: "大暑", 8: "处暑",
            9: "秋分", 10: "霜降", 11: "小雪", 12: "冬至"
        }
        return term_map.get(month, "春分")

    def _get_term_adjustment(self, term: str) -> float:
        """根据节气获取宫位起始点修正值（单位：小时）"""
        # 传统紫微斗数中不同节气命宫起算点不同
        adjust_map = {
            "大寒": 0.5, "雨水": 1.0, "春分": 1.5, "谷雨": 2.0,
            "小满": 2.5, "夏至": 3.0, "大暑": 3.5, "处暑": 4.0,
            "秋分": 4.5, "霜降": 5.0, "小雪": 5.5, "冬至": 6.0
        }
        return adjust_map.get(term, 1.5)  # 默认为春分修正值

    def _calculate_body_palace(self, life_palace: str, lunar: Lunar, gender: str) -> str:
        """
        优化身宫计算：
        1. 结合性别调整身宫算法
        2. 考虑农历出生时辰
        """
        life_idx = ZIWEI_CONFIG["palaces"].index(life_palace)
        month = lunar.month
        hour = lunar.hour if hasattr(lunar, 'hour') else 12  # 默认为午时

        # 身宫 = (命宫位置 + 出生月份 + 性别修正 + 时辰修正) % 12
        gender_adjust = 0 if gender == "male" else 6
        hour_adjust = (hour // 2) % 12  # 时辰每2小时对应一个宫位

        body_idx = (life_idx + month + gender_adjust + hour_adjust) % 12
        return ZIWEI_CONFIG["palaces"][body_idx]

    # === 主星排盘算法完整实现 ===
    def _calculate_major_stars(self, jd: float, life_palace: str, lunar: Lunar,
                               longitude: float, latitude: float) -> dict:
        """
        完整主星排盘算法（紫微斗数十四主星排盘规则）：
        1. 紫微星定位（根据农历年干和月支）
        2. 天府星定位（与紫微星相对）
        3. 其他主星按固定规则排布
        """
        # 初始化12宫位主星分布
        stars_in_palaces = {palace: [] for palace in ZIWEI_CONFIG["palaces"]}

        # 1. 计算紫微星位置（根据年干和月支）
        year_stem = self._get_lunar_year_stem(lunar.year)
        month_branch = EARTHLY_BRANCHES[(lunar.month - 1) % 12]
        ziwei_idx = self._calculate_ziwei_position(year_stem, month_branch)
        stars_in_palaces[ZIWEI_CONFIG["palaces"][ziwei_idx]].append("紫微")

        # 2. 天府星位置（与紫微星相差4宫）
        tianfu_idx = (ziwei_idx + 4) % 12
        stars_in_palaces[ZIWEI_CONFIG["palaces"][tianfu_idx]].append("天府")

        # 3. 太阳系主星定位（太阳、太阴等）
        sun_pos = self._get_planet_position(jd, swe.SUN)
        moon_pos = self._get_planet_position(jd, swe.MOON)
        sun_palace = self._position_to_palace(sun_pos, life_palace)
        moon_palace = self._position_to_palace(moon_pos, life_palace)

        stars_in_palaces[sun_palace].append("太阳")
        stars_in_palaces[moon_palace].append("太阴")

        # 4. 其他主星排布（按紫微斗数规则）
        # 天机星：命宫起寅，顺时针排布
        tianji_idx = (ZIWEI_CONFIG["palaces"].index(life_palace) + 2) % 12
        stars_in_palaces[ZIWEI_CONFIG["palaces"][tianji_idx]].append("天机")

        # 武曲星：命宫起辰，逆时针排布
        wuqu_idx = (ZIWEI_CONFIG["palaces"].index(life_palace) + 5) % 12
        stars_in_palaces[ZIWEI_CONFIG["palaces"][wuqu_idx]].append("武曲")

        # 天同星：命宫起午，顺时针排布
        tiantong_idx = (ZIWEI_CONFIG["palaces"].index(life_palace) + 7) % 12
        stars_in_palaces[ZIWEI_CONFIG["palaces"][tiantong_idx]].append("天同")

        # 廉贞星：与天同星同宫
        stars_in_palaces[ZIWEI_CONFIG["palaces"][tiantong_idx]].append("廉贞")

        # 贪狼星：紫微星起子，顺时针数至月支
        tanlang_idx = self._calculate_tanlang_position(ziwei_idx, month_branch)
        stars_in_palaces[ZIWEI_CONFIG["palaces"][tanlang_idx]].append("贪狼")

        # 巨门星：贪狼星+1宫
        jumen_idx = (tanlang_idx + 1) % 12
        stars_in_palaces[ZIWEI_CONFIG["palaces"][jumen_idx]].append("巨门")

        # 天相星：天府星+1宫
        tianxiang_idx = (tianfu_idx + 1) % 12
        stars_in_palaces[ZIWEI_CONFIG["palaces"][tianxiang_idx]].append("天相")

        # 天梁星：天相星+1宫
        tianliang_idx = (tianxiang_idx + 1) % 12
        stars_in_palaces[ZIWEI_CONFIG["palaces"][tianliang_idx]].append("天梁")

        # 七杀星：紫微星对宫
        qisha_idx = (ziwei_idx + 6) % 12
        stars_in_palaces[ZIWEI_CONFIG["palaces"][qisha_idx]].append("七杀")

        # 破军星：七杀星+1宫
        pojun_idx = (qisha_idx + 1) % 12
        stars_in_palaces[ZIWEI_CONFIG["palaces"][pojun_idx]].append("破军")

        # 5. 处理空宫情况
        for palace in stars_in_palaces:
            if not stars_in_palaces[palace]:
                stars_in_palaces[palace].append("空宫")

        return stars_in_palaces

    def _get_lunar_year_stem(self, lunar_year: int) -> str:
        """获取农历年干（用于紫微星定位）"""
        # 简化算法：实际应使用干支转换
        stem_idx = (lunar_year - 1900) % 10
        return HEAVENLY_STEMS[stem_idx]

    def _calculate_ziwei_position(self, year_stem: str, month_branch: str) -> int:
        """
        计算紫微星位置（根据年干和月支）：
        甲年起亥，乙年起午，丙年起寅，丁年起酉，
        戊年起卯，己年起子，庚年起申，辛年起辰，
        壬年起未，癸年起丑
        """
        ziwei_map = {
            "甲": 11, "乙": 6, "丙": 2, "丁": 9,
            "戊": 3, "己": 0, "庚": 8, "辛": 4,
            "壬": 7, "癸": 1
        }
        branch_idx = EARTHLY_BRANCHES.index(month_branch)
        base_idx = ziwei_map.get(year_stem, 0)
        return (base_idx + branch_idx) % 12

    def _calculate_tanlang_position(self, ziwei_idx: int, month_branch: str) -> int:
        """计算贪狼星位置（紫微星起子，顺时针数至月支）"""
        branch_idx = EARTHLY_BRANCHES.index(month_branch)
        return (ziwei_idx + branch_idx) % 12

    def _get_planet_position(self, jd: float, planet: int) -> float:
        """获取行星黄经位置（单位：度）"""
        _, pos = swe.calc_ut(jd, planet)
        return pos % 360  # 转换为0-360度

    def _position_to_palace(self, position: float, life_palace: str) -> str:
        """将黄经位置转换为紫微宫位"""
        life_idx = ZIWEI_CONFIG["palaces"].index(life_palace)
        palace_idx = int(position / 30) % 12  # 每30度一个宫位
        return ZIWEI_CONFIG["palaces"][(life_idx + palace_idx) % 12]

    # === 辅星排盘算法完整实现 ===
    def _calculate_minor_stars(self, jd: float, lunar: Lunar, life_palace: str) -> dict:
        """
        完整辅星排盘算法：
        1. 文昌文曲（根据出生日干和时支）
        2. 左辅右弼（根据出生年干和月支）
        3. 天魁天钺（根据出生年干）
        4. 禄存天马（根据日干和时支）
        5. 煞星（擎羊陀罗火星铃星等地空劫）
        """
        minor_stars = {star: "空宫" for star in ZIWEI_CONFIG["minor_stars"]}

        # 1. 文昌文曲星（日干起子，顺时针排至时支）
        day_stem = self._get_lunar_day_stem(lunar)
        hour_branch = EARTHLY_BRANCHES[(lunar.hour if hasattr(lunar, 'hour') else 12) // 2]

        wenchang_idx = self._calculate_wenchang_position(day_stem, hour_branch)
        minor_stars["文昌"] = ZIWEI_CONFIG["palaces"][wenchang_idx]

        wenqu_idx = (wenchang_idx + 2) % 12
        minor_stars["文曲"] = ZIWEI_CONFIG["palaces"][wenqu_idx]

        # 2. 左辅右弼星（年干起子，左辅顺排，右弼逆排至月支）
        year_stem = self._get_lunar_year_stem(lunar.year)
        month_branch = EARTHLY_BRANCHES[(lunar.month - 1) % 12]

        zuofu_idx = self._calculate_zuofu_position(year_stem, month_branch)
        minor_stars["左辅"] = ZIWEI_CONFIG["palaces"][zuofu_idx]

        youbi_idx = self._calculate_youbi_position(year_stem, month_branch)
        minor_stars["右弼"] = ZIWEI_CONFIG["palaces"][youbi_idx]

        # 3. 天魁天钺星（年干对应贵人宫）
        tiankui_idx, tianyue_idx = self._calculate_tiankui_tianyue(year_stem)
        minor_stars["天魁"] = ZIWEI_CONFIG["palaces"][tiankui_idx]
        minor_stars["天钺"] = ZIWEI_CONFIG["palaces"][tianyue_idx]

        # 4. 禄存星（日干起寅，顺时针排至时支）
        luxun_idx = self._calculate_luxun_position(day_stem, hour_branch)
        minor_stars["禄存"] = ZIWEI_CONFIG["palaces"][luxun_idx]

        # 5. 天马星（根据出生年支）
        year_branch = EARTHLY_BRANCHES[(lunar.year - 1900) % 12]
        tianma_idx = self._calculate_tianma_position(year_branch)
        minor_stars["天马"] = ZIWEI_CONFIG["palaces"][tianma_idx]

        # 6. 煞星（擎羊陀罗火星铃星）
        qingyang_idx = self._calculate_qingyang_position(lunar)
        minor_stars["擎羊"] = ZIWEI_CONFIG["palaces"][qingyang_idx]

        tuoluo_idx = (qingyang_idx + 1) % 12
        minor_stars["陀罗"] = ZIWEI_CONFIG["palaces"][tuoluo_idx]

        huoxing_idx = self._calculate_huoxing_position(lunar)
        minor_stars["火星"] = ZIWEI_CONFIG["palaces"][huoxing_idx]

        lingxing_idx = self._calculate_lingxing_position(lunar)
        minor_stars["铃星"] = ZIWEI_CONFIG["palaces"][lingxing_idx]

        # 7. 空劫星（地空地劫）
        dikong_idx = self._calculate_dikong_position(lunar)
        minor_stars["地空"] = ZIWEI_CONFIG["palaces"][dikong_idx]

        dijie_idx = (dikong_idx + 6) % 12
        minor_stars["地劫"] = ZIWEI_CONFIG["palaces"][dijie_idx]

        return minor_stars

    def _get_lunar_day_stem(self, lunar: Lunar) -> str:
        """获取农历日干（简化算法，实际应使用干支纪日）"""
        # 简化处理，实际应使用更精确的干支纪日算法
        stem_idx = (lunar.day + lunar.month + lunar.year) % 10
        return HEAVENLY_STEMS[stem_idx]

    def _calculate_wenchang_position(self, day_stem: str, hour_branch: str) -> int:
        """计算文昌星位置"""
        stem_map = {"甲": 0, "乙": 5, "丙": 10, "丁": 3, "戊": 8,
                    "己": 1, "庚": 6, "辛": 11, "壬": 4, "癸": 9}
        branch_idx = EARTHLY_BRANCHES.index(hour_branch)
        return (stem_map.get(day_stem, 0) + branch_idx) % 12

    def _calculate_zuofu_position(self, year_stem: str, month_branch: str) -> int:
        """计算左辅星位置（顺排）"""
        stem_map = {"甲": 0, "乙": 1, "丙": 2, "丁": 3, "戊": 4,
                    "己": 5, "庚": 6, "辛": 7, "壬": 8, "癸": 9}
        branch_idx = EARTHLY_BRANCHES.index(month_branch)
        return (stem_map.get(year_stem, 0) + branch_idx) % 12

    def _calculate_youbi_position(self, year_stem: str, month_branch: str) -> int:
        """计算右弼星位置（逆排）"""
        stem_map = {"甲": 0, "乙": 11, "丙": 10, "丁": 9, "戊": 8,
                    "己": 7, "庚": 6, "辛": 5, "壬": 4, "癸": 3}
        branch_idx = EARTHLY_BRANCHES.index(month_branch)
        return (stem_map.get(year_stem, 0) + branch_idx) % 12

    def _calculate_tiankui_tianyue(self, year_stem: str) -> tuple:
        """计算天魁天钺星位置（年干贵人）"""
        tiankui_map = {"甲": 11, "乙": 10, "丙": 1, "丁": 0, "戊": 11,
                       "己": 10, "庚": 5, "辛": 4, "壬": 3, "癸": 2}
        tianyue_map = {"甲": 1, "乙": 0, "丙": 11, "丁": 10, "戊": 1,
                       "己": 0, "庚": 7, "辛": 6, "壬": 5, "癸": 4}
        return tiankui_map.get(year_stem, 0), tianyue_map.get(year_stem, 6)

    # === 五行局与大限计算优化 ===
    def _calculate_wuxing_bureau(self, lunar: Lunar, major_stars: dict) -> str:
        """
        优化五行局计算：
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

    def _get_nayin_wuxing(self, stem: str, branch: str) -> str:
        """获取年干支纳音五行（简化算法）"""
        # 实际应使用完整的纳音五行表
        stem_idx = HEAVENLY_STEMS.index(stem)
        branch_idx = EARTHLY_BRANCHES.index(branch)
        nayin_index = (stem_idx * 12 + branch_idx) % 5
        wuxing_list = ["金", "火", "木", "水", "土"]
        return wuxing_list[nayin_index]

    def _get_star_wuxing(self, stars: list) -> str:
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


def _calculate_major_limits(self, wuxing_bureau: str, life_palace: str,
                            gender: str, lunar: Lunar) -> list:
    """
    精确大限计算：
    1. 起限年龄根据五行局和出生日干
    2. 大限宫位移动方向根据性别
    3. 大限时长根据五行局
    """
    # 1. 计算起限年龄
    start_age = self._calculate_limit_start_age(wuxing_bureau, lunar)

    # 2. 确定大限宫位移动方向（男顺女逆）
    direction = 1 if gender == "male" else -1

    # 3. 确定大限时长（年）
    duration_map = {
        "水二局": 6, "木三局": 7, "金四局": 8,
        "土五局": 9, "火六局": 10
    }
    duration = duration_map.get(wuxing_bureau, 9)

    # 4. 计算大限宫位起始点
    life_idx = ZIWEI_CONFIG["palaces"].index(life_palace)
    current_idx = life_idx

    # 5. 生成大限列表
    major_limits = []
    current_age = start_age

    for i in range(12):
        palace = ZIWEI_CONFIG["palaces"][current_idx]
        major_limits.append({
            "palace": palace,
            "start_age": current_age,
            "end_age": current_age + duration - 1,
            "duration": duration
        })

        current_age += duration
        current_idx = (current_idx + direction) % 12

    return major_limits


def _calculate_limit_start_age(self, wuxing_bureau: str, lunar: Lunar) -> int:
    """计算大限起限年龄（结合五行局和出生日干）"""
    base_age_map = {
        "水二局": 4, "木三局": 6, "金四局": 8,
        "土五局": 10, "火六局": 12
    }
    base_age = base_age_map.get(wuxing_bureau, 10)

    # 结合日干进一步调整
    day_stem = self._get_lunar_day_stem(lunar)
    stem_adj_map = {"甲": 0, "乙": 1, "丙": 2, "丁": 3, "戊": 4,
                    "己": 0, "庚": 1, "辛": 2, "壬": 3, "癸": 4}
    adj = stem_adj_map.get(day_stem, 0)

    return base_age + adj


# === 其他辅助方法 ===
def _analyze_fortune_trend(self, major_stars: dict, minor_stars: dict, jd: float, wuxing_bureau: str) -> dict:
    """
    优化运势分析：
    1. 结合主星和辅星吉凶
    2. 考虑五行局与流年五行生克
    3. 分析四化星影响
    """
    current_year = swe.revjul(jd)[0]
    year_palace_idx = (current_year % 12)
    year_palace = ZIWEI_CONFIG["palaces"][year_palace_idx]

    # 1. 获取流年命宫主星
    year_stars = major_stars.get(year_palace, [])

    # 2. 获取流年命宫辅星
    year_minor_stars = [star for star, loc in minor_stars.items()
                        if loc == year_palace and star not in ["擎羊", "陀罗", "火星", "铃星", "地空", "地劫"]]
    year_sha_stars = [star for star, loc in minor_stars.items()
                if loc == year_palace and star in ["擎羊", "陀罗", "火星", "铃星", "地空", "地劫"]]

    # 3. 计算流年五行
    year_stem = HEAVENLY_STEMS[(current_year - 1900) % 10]
    year_wuxing = WUXING_MAP.get(year_stem, "")
    bureau_wuxing = wuxing_bureau[0]  # 五行局首字为五行属性

    # 4. 分析五行生克
    wuxing_relation = self._analyze_wuxing_relation(year_wuxing, bureau_wuxing)

    # 5. 综合判断运势
    fortune_level = self._determine_fortune_level(year_stars, year_minor_stars, year_sha_stars, wuxing_relation)

    # 6. 生成详细分析
    analysis = self._generate_fortune_analysis(current_year, year_palace, year_stars,
                                               year_minor_stars, year_sha_stars, wuxing_relation, fortune_level)

    return {
        "year": current_year,
        "year_palace": year_palace,
        "year_stars": year_stars,
        "year_minor_stars": year_minor_stars,
        "year_sha_stars": year_sha_stars,
        "wuxing_relation": wuxing_relation,
        "fortune_level": fortune_level,
        "analysis": analysis
    }


def _analyze_wuxing_relation(self, year_wuxing: str, bureau_wuxing: str) -> str:
    """分析流年五行与五行局的生克关系"""
    if not year_wuxing or not bureau_wuxing:
        return "平"

    wuxing_relations = {
        "木": {"生": "火", "克": "土", "被生": "水", "被克": "金"},
        "火": {"生": "土", "克": "金", "被生": "木", "被克": "水"},
        "土": {"生": "金", "克": "水", "被生": "火", "被克": "木"},
        "金": {"生": "水", "克": "木", "被生": "土", "被克": "火"},
        "水": {"生": "木", "克": "火", "被生": "金", "被克": "土"}
    }

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


# 使用示例（优化输出格式）
if __name__ == "__main__":
    print("紫微斗数计算系统 - 启动 (优化版)")

    # 创建计算器（自动更新星历表）
    calculator = ZiWeiCalculator(auto_update_ephe=True)

    # 示例输入数据（增加时区）
    birth_data = {
        "birth_datetime": "1990-05-15T14:30:00",
        "gender": "male",
        "timezone": "Asia/Shanghai"
    }

    location_data = {
        "longitude": 116.4,  # 北京经度
        "latitude": 39.9  # 北京纬度
    }

    # 执行计算
    try:
        print("开始计算紫微斗数命盘...")
        result = calculator.calculate(birth_data, location_data)

        # 输出结果（优化显示）
        print("\n=== 命盘基本信息 ===")
        print(f"出生时间: {result['basic_info']['birth_datetime']}")
        print(f"真太阳时: {result['basic_info']['true_solar_time']}")
        print(f"农历日期: {result['basic_info']['lunar_date']}")
        print(f"命宫: {result['palaces']['life_palace']}")
        print(f"身宫: {result['palaces']['body_palace']}")
        print(f"五行局: {result['wuxing_bureau']}")

        print("\n=== 大限分布 ===")
        for i, limit in enumerate(result["major_limits"][:5]):  # 显示前5个大限
            print(f"第{i + 1}大限: {limit['start_age']}-{limit['end_age']}岁，{limit['palace']}宫")

        print("\n=== 流年运势 ===")
        print(f"{result['fortune_trend']['year']}年运势分析:")
        print(f"流年命宫: {result['fortune_trend']['year_palace']}")
        print(f"主星: {', '.join(result['fortune_trend']['year_stars'])}")
        print(f"辅星: {', '.join(result['fortune_trend']['year_minor_stars'])}")
        print(f"煞星: {', '.join(result['fortune_trend']['year_sha_stars'])}")
        print(f"五行关系: {result['fortune_trend']['wuxing_relation']}")
        print(f"运势等级: {result['fortune_trend']['fortune_level']}")
        print(f"运势分析: {result['fortune_trend']['analysis']}")

        print("\n=== 命盘图 ===")
        print(result["chart"])

        # 保存完整结果
        with open("ziwei_result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("完整结果已保存到 ziwei_result.json")

    except Exception as e:
        print(f"计算失败: {str(e)}")