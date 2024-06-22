from flet_core import *

BG = "#1f262f"


class Profile(Container):

    def __init__(self):
        super().__init__(bgcolor=colors.BLACK, width=360, height=700)
        self.head = Container()
        self.nickname = Text(selectable=True, color=colors.WHITE, overflow=TextOverflow.ELLIPSIS, max_lines=3,
                             text_align=TextAlign.JUSTIFY)
        self.width = 700
        self.height = 100
        self.border_radius = 35
        self.bgcolor = BG
        self.padding = padding.only(
            left=20,
            top=20,
        )
        self.alignment = alignment.center
        self.content = Row(
            vertical_alignment=CrossAxisAlignment.STRETCH,
            spacing=1,
            run_spacing=1,
            controls=[
                Column([self.head]),
                Container(width=20),
                Container(alignment=alignment.top_center, content=self.nickname, width=400, height=30)
            ]
        )
