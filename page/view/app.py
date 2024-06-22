from flet_core import UserControl, Page, ResponsiveRow, MainAxisAlignment, CrossAxisAlignment


class App(UserControl):
    def __init__(self, page: Page):
        self.page = page
        self.row = ResponsiveRow(
            alignment=MainAxisAlignment.CENTER,
            vertical_alignment=CrossAxisAlignment.CENTER
        )
        super().__init__()

    def build(self):
        return self.row
