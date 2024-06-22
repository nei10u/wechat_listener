from flet_core import Card, Container, alignment, Text, TextAlign, colors, border, Page, FilledButton, Column, \
    MainAxisAlignment, CrossAxisAlignment
from flet_core.charts.bar_chart import BarChart
from flet_core.charts.bar_chart_group import BarChartGroup
from flet_core.charts.bar_chart_rod import BarChartRod
from flet_core.charts.chart_axis import ChartAxis
from flet_core.charts.chart_axis_label import ChartAxisLabel
from flet_core.charts.chart_grid_lines import ChartGridLines


class AddressBookKit(Card):

    def __init__(self, page: Page, imtool, address_book, _up, _down):
        super().__init__()
        self.page = page
        self.imtool = imtool
        self.address_book = address_book
        self._up = _up
        self._down = _down
        self.content = Container(
            content=Text(address_book['NickName'], color='white', text_align=TextAlign.CENTER, size=10),
            alignment=alignment.center,
            height=40,
            width=150,
            border_radius=10,
            bgcolor=colors.BLACK,
            on_hover=lambda e: change_bg_color(e),
            on_click=lambda _: self.show_info()
        )

    def show_info(self):
        self.change_chart()
        self.chat_entry()

    def change_chart(self):
        member_list = self.imtool.get_room_member_list(self.address_book['UserName'])
        print(f"member_list:{member_list}")
        chart = build_sex_chart(member_list)
        print(f"chart:{chart}")
        self._up.setContent(chart)
        self._up.update()

    def enter_chat_room(self):
        # 需要清理掉chart的内容，否则页面会有错误。
        self._up.setContent(None)
        print(f"group_name:{self.address_book['NickName']}")
        self.page.session.set("group_name", self.address_book['NickName'])
        self.page.go("/chatroom")

    def chat_entry(self):
        self._down.setContent(
            Column(
                expand=True,
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Text("接收信息", color=colors.WHITE),
                    FilledButton(
                        text=f"{self.address_book['NickName']}",
                        width=320,
                        height=80,
                        on_click=lambda _: self.enter_chat_room()
                    )]
            ))
        self._down.update()


def change_bg_color(e):
    e.control.bgcolor = colors.BLUE if e.data == "true" else colors.BLACK
    e.control.update()


def build_sex_chart(member_list):
    """
    :rtype: object
    """
    male = 0
    female = 0
    for member in member_list:
        if member['Sex'] == 1:
            male += 1
        elif member['Sex'] == 2:
            female += 1
    max_y = max(male, female) + 10
    y_labels = [
        ChartAxisLabel(
            value=i, label=Text(str(i), color=colors.WHITE)
        ) for i in range(0, max_y + 1, 10)  # 每隔10生成一个刻度
    ]
    return BarChart(
        bgcolor=colors.GREEN,
        bar_groups=[
            BarChartGroup(
                x=0,
                bar_rods=[
                    BarChartRod(
                        from_y=0,
                        to_y=male,
                        width=40,
                        color=colors.BROWN_900,
                        tooltip="Male",
                        border_radius=0,
                    ),
                ],
            ),
            BarChartGroup(
                x=1,
                bar_rods=[
                    BarChartRod(
                        from_y=0,
                        to_y=female,
                        width=40,
                        color=colors.BLUE,
                        tooltip="Female",
                        border_radius=0,
                    ),
                ],
            )
        ],
        border=border.all(1, colors.WHITE),
        left_axis=ChartAxis(
            show_labels=True, labels_size=40, title=Text("性别", color=colors.WHITE, rotate=40), title_size=40,
            labels=y_labels
        ),
        bottom_axis=ChartAxis(
            labels=[
                ChartAxisLabel(
                    value=0, label=Container(Text("男", color=colors.WHITE), padding=10)
                ),
                ChartAxisLabel(
                    value=1, label=Container(Text("女", color=colors.WHITE), padding=10)
                )
            ],
            labels_size=40,
        ),
        horizontal_grid_lines=ChartGridLines(
            color=colors.WHITE, width=1, dash_pattern=[3, 3]
        ),
        tooltip_bgcolor=colors.with_opacity(0.5, colors.WHITE),
        max_y=max_y,
        interactive=True,
        expand=True,
    )
