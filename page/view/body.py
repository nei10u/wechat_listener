from flet_core import Column, MainAxisAlignment, CrossAxisAlignment, Container, padding

chat_room_group = Column(
    wrap=True,
    spacing=8,
    run_spacing=8,
    height=200,
    auto_scroll=True,
    alignment=MainAxisAlignment.START,
    horizontal_alignment=CrossAxisAlignment.START
)

BG = "#041955"


class Body(Container):

    def __init__(self):
        super().__init__()
        self.chat_room_group = chat_room_group
        self.content = chat_room_group
        self.border_radius = 35
        self.width = 700
        self.bgcolor = BG
        self.padding = padding.only(
            left=20,
            top=20,
        )
