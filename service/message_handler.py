import time

from firebase_config import initialize_firebase
from service.imtool.lib import itchat

db = initialize_firebase()


# @singleton
class MessageHandler:

    def __init__(self, chatroom=None):
        self.chatroom = chatroom
        self.stream = None
        self.session_id = itchat.instance.storageClass.nickName

    def get_message_val(self, *args):
        session_id = itchat.instance.storageClass.nickName
        fn = db.child(session_id)
        for arg in args:
            fn.child(arg)
        return fn.get().val()

    def get_message_from_db(self, group_name):
        try:
            keys = list(self.get_message_val(group_name).keys())
            print(f"keys:{keys}")
            sorted_keys = sorted(keys, key=lambda x: int(x))
            return sorted_keys
        except Exception as e:
            return []

    def push_message_to_db(self, cmsg):
        try:
            data = {
                "sys_timestamp": int(time.time() * 1000),
                "msg_create_time": cmsg.create_time,
                "msg_id": cmsg.msg_id,
                "msg_type": str(cmsg.ctype),
                "msg_content": cmsg.content,
                "from_user_id": cmsg.actual_user_id if cmsg.is_group else cmsg.from_user_id,
                "from_user_nickname": cmsg.actual_user_nickname if cmsg.is_group else cmsg.from_user_nickname,
                "to_user_id": '' if cmsg.is_group else cmsg.to_user_id,
                "to_user_nickname": cmsg.other_user_nickname if cmsg.is_group else cmsg.to_user_nickname,
                "is_group": cmsg.is_group,
                "group_display_name": cmsg.self_display_name,
                "is_at": cmsg.is_at,
                "actual_user_id": str(cmsg.at_list)
            }

            to_user_id = cmsg.other_user_nickname if cmsg.is_group else cmsg.to_user_nickname
            print(f"session_id:{self.session_id}")
            print(f"data:{data}")
            db.child(self.session_id).child(to_user_id).child(int(time.time())).set(data)
        except Exception as e:
            print(e)

    def start_history(self, group_name):
        sorted_keys = self.get_message_from_db(group_name)
        items = []
        if sorted_keys is not None:
            for key in sorted_keys:
                value = self.get_message_val(group_name, key)
                items.append(self.chatroom.chat_history(value))
        self.chatroom.render_chat_arena(items)

    def start_listener(self, group_name):
        self.stream = db.child(self.session_id).child(group_name).stream(self.chatroom.chat_stream)

# if __name__ == "__main__":
#     MessageHandler("test", "1234567890", "USER").push_message_to_db()
