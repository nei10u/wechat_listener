import pyrebase


def initialize_firebase():
    config = {
        "apiKey": "AIzaSyADLO7hPnF7w7cIOHRYd1RcUAuywqLvl4Q",
        "authDomain": "",
        "databaseURL": "https://wechat-listener-default-rtdb.firebaseio.com/",
        "storageBucket": ""
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    return db
