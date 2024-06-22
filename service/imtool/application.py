from service.imtool.channel.wechat_channel import WechatChannel
from service.imtool.common.log import logger
from service.imtool.lib import itchat


class IMTool:
    channel_type = ""

    def __init__(self, channel_type, mock_data=None):
        self.channel_type = channel_type
        self.mock_data = mock_data

    def run(self, render):
        if self.mock_data is None:
            try:
                # TODO: add a ChannelFactory to init channel by self.channel_type
                channel = WechatChannel()
                channel.startup(render.qr_callback, render.login_callback)
            except Exception as e:
                logger.error("App startup failed!")
                logger.exception(e)
        else:
            render.qr_callback(-1, "-100", self.mock_data.login_info)
            # render.login_callback(self.mock_data.login_info)

    def get_head_img(self, user_name):
        if self.mock_data is None:
            return itchat.get_head_img(userName=user_name)
        else:
            return self.mock_data.mock_avatar()

    def get_room_list(self):
        if self.mock_data is None:
            return itchat.instance.chatroomList
        else:
            return self.mock_data.chat_rooms

    def get_room_member_list(self, user_name):
        if self.mock_data is None:
            print(f"user_name:{user_name}")
            itchat.instance.update_chatroom(userName=user_name, detailedMember=True)
            find = False
            for chatroom in itchat.instance.chatroomList:
                if user_name == chatroom["UserName"]:
                    find = True
                    break
            if find:
                return chatroom["MemberList"]
            else:
                return []
        else:
            return self.mock_data.chat_room_members
