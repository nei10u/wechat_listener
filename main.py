from flet import *

# from mock.mock import MockData
from page.home import Home
from page.login import Login
from page.chatroom import ChatRoom
from service.imtool.application import IMTool

view_style = {
    "bgcolor": "#1f2128",
    "padding": 30,
}


class Main(Stack):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.on_error = lambda e: print("Page error:", e.data, e.name, e.target)
        # self.imtool = IMTool('wx', MockData('mock'))
        self.imtool = IMTool('wx')
        self.init_helper()

    def init_helper(self):
        self.page.on_route_change = self.on_route_change
        self.page.go('/login')

    def on_route_change(self, route):
        # 不能在new_page页面对象初始化时跳转，否则会页面嵌套，无法正常展示。
        print(f"route:{route}")

        new_page = {
            "/login": Login,
            "/home": Home,
            "/chatroom": ChatRoom,
        }[self.page.route](self.page, self.imtool)

        if self.page.route != '/login':
            print(f"new_page.content:{new_page.content}")
            print(f"1:{self.page.views}")
            self.page.views.clear()
            view_style.update(route=route, controls=[new_page])
            self.page.views.append(
                View(**view_style)
            )
            print(f"2:{self.page.views}")
            self.page.update()


if __name__ == "__main__":
    app(target=Main, assets_dir='assets')

# def main(page: Page):
#     # imtool = IMTool('wx')
#     profile = Profile()
#     body = Body()
#     alert = Alert()
#     # 设置页面的对齐方式
#     page.window_width = 700
#     page.window_height = 800
#     # page.window_resizable = False
#     page.vertical_alignment = MainAxisAlignment.CENTER
#     page.horizontal_alignment = CrossAxisAlignment.CENTER
#     page.padding = 35
#     theme = Theme(
#         scrollbar_theme=ScrollbarTheme(thickness=3,
#                                        radius=10,
#                                        main_axis_margin=-20,
#                                        thumb_color="#64b687"
#                                        )
#     )
#     page.theme = theme
#     page.on_error = lambda e: print("Page error:", e.data, e.name, e.target)
#     imtool = IMTool('wx', mock_data=MockData('mock'))
#     app = App(page)
#     page.add(app)
#     render = Render(imtool, page, profile, body, alert)
#     imtool.run(render)
#
#
# if __name__ == "__main__":
#     app(target=main, assets_dir='assets')
