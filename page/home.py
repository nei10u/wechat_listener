import base64

from flet import *
from flet_core.alignment import center

from page.view.avatar import AvatarKit
from page.view.address_book import AddressBookKit
from service.imtool.application import IMTool

profile_style = {
    "main": {
        "expand": True,
        "bgcolor": "#17181d",
        "border_radius": 10,
    }
}

info_style = {
    "expand": True,
    "bgcolor": "#17181d",
    "border_radius": 10,
    "padding": 30,
}


class GroupProfile(Container):
    def __init__(self, address_books):
        super().__init__(**profile_style.get("main"))
        self.content = AddressBookGroup(address_books)


class AddressBookGroup(ListView):
    def __init__(self, address_books):
        super().__init__()
        self.alignment = MainAxisAlignment.CENTER
        self.controls = address_books


class BasicProfile(Container):
    def __init__(self, page: Page, imtool, _up, _down, avatar_image, user_name, address_books_info):
        super().__init__(**profile_style.get("main"))
        address_books = []
        for address in address_books_info:
            address_books.append(AddressBookKit(page, imtool, address, _up, _down))

        self.content = Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Divider(height=15, color="transparent"),
                avatar_image,
                Text(value=user_name, size=16, color=colors.WHITE, weight=FontWeight.W_900, selectable=True),
                Divider(height=15, color="transparent"),
                Text(value="通讯录", size=16, color=colors.WHITE, weight=FontWeight.W_900, selectable=True),
                GroupProfile(address_books)
            ]
        )


class ChatRoomBasicInfo(Container):
    def __init__(self):
        super().__init__(**info_style)
        self.alignment = center

    def setContent(self, content):
        self.content = content


class ChatRoomEnter(Container):
    def __init__(self):
        super().__init__(**info_style)
        self.alignment = center

    def setContent(self, content):
        self.content = content


class Home(Container):

    def __init__(self, page: Page, imtool: IMTool):
        super().__init__()
        avatar_image = get_avatar(imtool, page.session.get("login_info")['User']['UserName'])
        print(f"avatar_image:{avatar_image}")
        # ------
        chat_rooms_info = imtool.get_room_list()
        chat_room_basic_info = ChatRoomBasicInfo()
        chat_room_entry = ChatRoomEnter()
        basic_profile = BasicProfile(page, imtool, chat_room_basic_info, chat_room_entry, avatar_image,
                                     page.session.get("login_info")['User']["NickName"],
                                     chat_rooms_info)
        self.expand = True
        self.content = Row(
            expand=True,
            controls=[
                Column(
                    expand=True,
                    controls=[basic_profile]
                ),
                Column(
                    expand=True,
                    controls=[chat_room_basic_info, chat_room_entry]
                )
            ]
        )


def get_avatar(imtool, user_name):
    avatar = imtool.get_head_img(user_name)
    with open("assets/images/avatar.png", 'wb') as f:
        f.write(avatar)
    avatar = base64.b64encode(avatar).decode('utf-8')
    return AvatarKit(avatar)
