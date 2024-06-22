from datetime import datetime

from flet_core import Container, colors, Page, Column, TextField, Card, alignment, padding, Text, Divider, border, \
    Row, MainAxisAlignment, ScrollMode, icons, Icon, ElevatedButton, transform, FontWeight, CrossAxisAlignment, Stack, \
    FloatingActionButton

from service.imtool.application import IMTool
from service.imtool.lib import itchat
from service.message_handler import MessageHandler


class ChatRoom(Container):

    def __init__(self, page: Page, imtool: IMTool):
        super().__init__()
        self.page = page
        self.message_handler = MessageHandler(self)
        self.expand = True
        self.arena = self.chat_arena()
        self.content = Column(
            expand=True,
            controls=[
                Stack(controls=[self.chat_header(self.page.session.get("group_name")), self.back_btn()]),
                Divider(height=2, color='transparent'),
                Container(
                    expand=True,
                    border=border.only(
                        bottom=border.BorderSide(1.25, "white")
                    ),
                    content=self.arena
                ),
                Divider(height=2, color='transparent'),
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[self.send_text_btn()]
                )
            ]
        )
        self.message_handler.start_history(self.page.session.get("group_name"))
        self.count = 0
        self.message_handler.start_listener(self.page.session.get("group_name"))
        print(f"__init__ invoke, count:{self.count}")

    def render_chat_arena(self, items):
        print(f"items:{items}")
        self.arena.controls = items

    def chat_item_ui(self, value):
        print(f"1-value:{value}")
        if value is not None:
            sent_time = datetime.fromtimestamp(value['msg_create_time']).strftime("%H:%M")
            if value['from_user_nickname'] == itchat.instance.storageClass.nickName:
                return self.chat_message_ui(sent_time, value['from_user_nickname'], value['msg_content'],
                                            CrossAxisAlignment.END,
                                            MainAxisAlignment.END, "teal100")
            else:
                return self.chat_message_ui(sent_time, value['from_user_nickname'], value['msg_content'],
                                            CrossAxisAlignment.START,
                                            MainAxisAlignment.START, "blue100")

    def chat_history(self, value):
        return self.chat_item_ui(value)

    def chat_stream(self, value):
        items = []
        print(f"chat_stream-value:{value}")
        print(f"chat_stream-count:{self.count}")
        if value is not None:
            if self.count > 0:
                items.append(self.chat_item_ui(value))
                self.render_chat_arena(items)
            else:
                pass
            self.count += 1

    def back_btn(self):
        return FloatingActionButton(
            top=5, left=10, icon=icons.ARROW_LEFT, on_click=lambda _: self.page.go(
                '/home')
        )

    def chat_header(self, group_name):
        return Card(
            expand=True,
            height=65,
            elevation=10,
            margin=-10,
            content=Container(
                alignment=alignment.center,
                padding=padding.only(top=10),
                bgcolor="#202224",
                content=Text(group_name, color=colors.WHITE, weight=FontWeight.BOLD, size=21)
            )
        )

    def chat_arena(self):
        return Column(
            scroll=ScrollMode.HIDDEN,
            auto_scroll=True
        )

    def chat_input(self):
        return TextField(
            expand=True,
            # label_style=TextStyle(size=8, color=colors.BLACK, weight=FontWeight.BOLD),
            height=50,
            text_size=12,
            cursor_width=1,
            color=colors.WHITE,
            cursor_color=colors.WHITE,
            border_color=colors.WHITE,
            border_width=1,
            content_padding=8
        )

    def send_text_btn(self):
        return ElevatedButton(
            bgcolor=colors.WHITE,
            content=Icon(
                name=icons.SEND,
                size=13,
                color=colors.BLACK,
                rotate=transform.Rotate(5.5, alignment=alignment.center)
            )
        )

    def chat_message_ui(self, sent_time, name, text_message, col_pos, row_pos, bg):
        return Container(
            padding=padding.only(left=25, top=12, bottom=12, right=25),
            bgcolor=colors.GREEN_100,
            border_radius=8,
            margin=5,
            content=Column(
                horizontal_alignment=col_pos,
                spacing=5,
                controls=[
                    Row(
                        alignment=row_pos,
                        controls=[
                            Text(
                                name + "@" + sent_time,
                                color="black",
                                size=8,
                                weight="bold"
                            )
                        ]
                    ),
                    Row(
                        alignment=row_pos,
                        controls=[
                            Text(
                                text_message,
                                color="black",
                                size=15,
                            )
                        ]
                    ),
                ]
            )
        )
