import os
import time

from service.imtool.bridge.context import ContextType
from service.imtool.channel.chat_channel import ChatChannel
from service.imtool.channel.chat_message import ChatMessage
from service.imtool.channel.wechat.wechat_message import WechatMessage
from service.imtool.common.config import get_appdata_dir, conf
from service.imtool.common.log import logger
from service.imtool.common.singleton import singleton
from service.imtool.common.time_checker import time_checker
from service.imtool.lib import itchat
from service.imtool.lib.itchat.content import *
from service.message_handler import MessageHandler


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
def handler_group_msg(msg):
    try:
        cmsg = WechatMessage(msg, is_group=True)
        print(cmsg)
        MessageHandler().push_message_to_db(cmsg)
    except NotImplementedError as e:
        logger.debug("[WX]group message {} skipped: {}".format(msg["MsgId"], e))
        return None
    return None


def _check(func):
    def wrapper(self, cmsg: ChatMessage):
        msgId = cmsg.msg_id
        if msgId in self.receivedMsgs:
            logger.info("Wechat message {} already received, ignore".format(msgId))
            return
        self.receivedMsgs[msgId] = True
        create_time = cmsg.create_time  # 消息时间戳
        if conf().get("hot_reload") == True and int(create_time) < int(time.time()) - 60:  # 跳过1分钟前的历史消息
            logger.debug("[WX]history message {} skipped".format(msgId))
            return
        if cmsg.my_msg and not cmsg.is_group:
            logger.debug("[WX]my message {} skipped".format(msgId))
            return
        return func(self, cmsg)

    return wrapper


@singleton
class WechatChannel(ChatChannel):

    def startup(self, qr_callback, login_callback):
        itchat.instance.receivingRetryCount = 600  # 修改断线超时时间
        status_path = os.path.join(get_appdata_dir(), "itchat.pkl")
        itchat.auto_login(
            enableCmdQR=False,
            hotReload=False,
            statusStorageDir=status_path,
            qrCallback=qr_callback,
            loginCallback=login_callback
        )
        self.user_id = itchat.instance.storageClass.userName
        self.name = itchat.instance.storageClass.nickName
        logger.info("Wechat login success, user_id: {}, nickname: {}".format(self.user_id, self.name))
        # start message listener
        itchat.run(debug=True)

    @time_checker
    @_check
    def handle_group(self, cmsg: ChatMessage):
        if cmsg.ctype == ContextType.VOICE:
            if not conf().get("group_speech_recognition"):
                return
            logger.debug("[WX]receive voice for group msg: {}".format(cmsg.content))
        elif cmsg.ctype == ContextType.IMAGE:
            logger.debug("[WX]receive image for group msg: {}".format(cmsg.content))
        elif cmsg.ctype in [ContextType.JOIN_GROUP, ContextType.PATPAT, ContextType.ACCEPT_FRIEND, ContextType.EXIT_GROUP]:
            logger.debug("[WX]receive note msg: {}".format(cmsg.content))
        elif cmsg.ctype == ContextType.TEXT:
            # logger.debug("[WX]receive group msg: {}, cmsg={}".format(json.dumps(cmsg._rawmsg, ensure_ascii=False), cmsg))
            pass
        elif cmsg.ctype == ContextType.FILE:
            logger.debug(f"[WX]receive attachment msg, file_name={cmsg.content}")
        else:
            logger.debug("[WX]receive group msg: {}".format(cmsg.content))
        # context = self._compose_context(cmsg.ctype, cmsg.content, isgroup=True, msg=cmsg)
        # if context:
        #     self.produce(context)
