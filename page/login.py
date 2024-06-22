import base64

from flet import *

from service.imtool.application import IMTool


class Login(Container):

    def __init__(self, page: Page, imtool: IMTool):
        super().__init__()
        self.page = page
        self.imtool = imtool

        self.content = Text("Login")

        self.bg_loading = AlertDialog(
            content=Container(
                expand=True,
                content=ProgressRing(width=160, height=160, stroke_width=2),
                width=200,  # 设置宽度
                height=200,  # 设置高度
                alignment=alignment.center
            ),
            modal=True
        )

        self.qr_alert = AlertDialog(
            adaptive=True,
            title=Text("微信扫码登陆", text_align=TextAlign.CENTER),
            modal=True
        )

        self.im_startup()

    def im_startup(self):
        self.imtool.run(self)

    def qr_callback(self, uuid, status, data):
        print(uuid, status, data)
        if status == "-100":
            self.qr_alert.actions.append(TextButton("登录", on_click=lambda _: self.login_callback(data)))
            self.page.dialog = self.qr_alert
            self.qr_alert.open = True
        elif status == "200":
            self.qr_alert.open = False
            self.page.dialog = self.bg_loading
            self.bg_loading.open = True
        else:
            base64_image = base64.b64encode(data).decode('utf-8')
            self.qr_alert.content = Image(src_base64=base64_image)
            self.page.dialog = self.qr_alert
            self.qr_alert.open = True
        self.page.update()

    def login_callback(self, login_info):
        self.page.session.set("login_info", login_info)
        self.page.go("/home")
