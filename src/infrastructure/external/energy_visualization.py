import base64
import io
import numpy as np
import matplotlib.pyplot as plt
from src.domain.jewelry.value_objects import UserEnergyProfile, JewelryEnergySignature
import logging

logger = logging.getLogger(__name__)


class EnergyVisualizer:
    def generate_energy_chart(self, user_energy: UserEnergyProfile, jewelry_energy: JewelryEnergySignature) -> str:
        """
        生成用户与珠宝的五行能量对比图，并返回Base64编码的PNG图片。
        """
        elements = ['金', '木', '水', '火', '土']
        # 假设UserEnergyProfile和JewelryEnergySignature有get_element_value方法
        user_values = [user_energy.get_element_value(e) for e in elements]
        jewelry_values = [jewelry_energy.get_element_value(e) for e in elements]

        # 确保数据有效性
        if not all(isinstance(v, (int, float)) for v in user_values + jewelry_values):
            logger.error("Invalid energy values provided for chart generation.")
            raise ValueError("Energy values must be numeric.")

        fig, ax = plt.subplots(figsize=(10, 6))

        x = np.arange(len(elements))
        width = 0.35

        rects1 = ax.bar(x - width / 2, user_values, width, label='用户能量', color='#4CAF50')
        rects2 = ax.bar(x + width / 2, jewelry_values, width, label='珠宝能量', color='#2196F3')

        ax.set_ylabel('能量值')
        ax.set_title('五行能量匹配分析', fontsize=16)
        ax.set_xticks(x)
        ax.set_xticklabels(elements, fontsize=12)
        ax.legend(fontsize=10)
        ax.set_ylim(0, max(max(user_values), max(jewelry_values)) * 1.2)  # 动态Y轴范围

        # 添加数值标签
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)

        plt.tight_layout()  # 自动调整子图参数，使之填充整个图像区域

        # 保存为Base64编码的PNG图片
        buf = io.BytesIO()
        try:
            plt.savefig(buf, format='png', bbox_inches='tight')  # bbox_inches='tight' 避免标签被截断
            buf.seek(0)
            return base64.b64encode(buf.getvalue()).decode('utf-8')
        except Exception as e:
            logger.error(f"Failed to generate energy chart: {e}")
            raise RuntimeError("Failed to generate energy chart.")
        finally:
            plt.close(fig)  # 关闭图表，释放内存
