from flet_core import Container, Image, animation, colors


class AvatarKit(Container):

    def __init__(self, avatar):
        super().__init__()
        self.avatar = avatar
        self.on_hover = lambda x: scaleUpImage(x)
        self.scale = 1
        # self.animate_scale = animation.Animation(100, "bounceOut")
        # self.bgcolor = colors.BLUE
        self.content = Image(
            src_base64=self.avatar,
            width=60,
            height=60,
            border_radius=30,
        )


def scaleUpImage(x):
    if x.control.scale != 1.5:
        x.control.scale = 1.5
    else:
        x.control.scale = 1
    x.control.update()
