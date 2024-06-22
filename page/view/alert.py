from flet_core import AlertDialog, Image, Text, TextAlign, ClipBehavior


class Alert:

    def __init__(self):
        self.bg_loading = AlertDialog(
            adaptive=True,
            content=Image(src="images/loading_animation_loop.gif"),
            clip_behavio=ClipBehavior.HARD_EDGE,
            modal=True
        )

        self.qr_alert = AlertDialog(
            adaptive=True,
            title=Text("微信扫码登陆", text_align=TextAlign.CENTER),
            modal=True
        )
