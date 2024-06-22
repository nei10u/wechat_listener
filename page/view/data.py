from flet_core import UserControl, Control
import pandas as pd
from math import pi

from flet_core.charts.pie_chart import PieChart
from flet_core.charts.pie_chart_section import PieChartSection


class DataVisualizationKit(UserControl):
    def __init__(self):
        # self.friend_count: float = friend_count
        # self.group_count: float = group_count
        # self.color: str = color
        # self.chart: Control = PieChart(
        #     sections=[
        #         PieChartSection(value=self.friend_count, color=self.color, radius=15),
        #         PieChartSection(value=self.friend_count, color=self.color, radius=15),
        #     ]
        # )
        super.__init__()
