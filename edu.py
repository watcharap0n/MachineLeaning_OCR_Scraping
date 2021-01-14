from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import StickerSendMessage, TextSendMessage, TextMessage
import json
import pyrebase
from random import randrange

app = Flask(__name__)

with open('config/db_firebase.json', encoding='utf8') as config_file:
    data = json.load(config_file)
    config = data['firebase']
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    line_bot_api = LineBotApi(data['channel_secret_token'])
    handler = WebhookHandler(data['channel_secret'])


def log_line(val):
    with open('config/log.json', 'w') as log_line:
        json.dump(val, log_line)


def no_event(decoded):
    no_event = len(decoded['events'])
    for i in range(no_event):
        event = decoded['events'][i]
        event_handle(event)


@app.route('/webhook', methods=['POST'])
def webhook():
    raw_json = request.get_json()
    json_line = json.dumps(raw_json)
    decoded = json.loads(json_line)
    log_line(raw_json)
    event = decoded['events'][0]
    _type = event['type']
    if _type == 'follow':
        userId = event['source']['userId']
        profile = line_bot_api.get_profile(userId)
        displayName = profile.display_name
        img = profile.picture_url
        status = profile.status_message
        inserted = {'displayName': displayName, 'img': img, 'status': status, 'userId': userId}
        db.child('userId_follow').push(inserted)
    elif _type == 'unfollow':
        userId = event['source']['userId']
        remove = db.child('userId_follow').order_by_child('userId').equal_to(userId).get()
        remove = remove.val()
        remove = remove.keys()
        for i in remove:
            db.child('userId_follow').child(i).remove()
    elif _type == 'message':
        message = event['message']['type']
        no_event(decoded)
    return 'ok'


def event_handle(event):
    _type = event['message']['type']
    if _type == 'sticker':
        sticker_id = randrange(52002734, 52002773)
        reply = event['replyToken']
        sticker_message = StickerSendMessage(
            package_id=str(11537),
            sticker_id=str(sticker_id)
        )
        line_bot_api.reply_message(reply, sticker_message)



if __name__ == 'main':
    app.run(port=5000, debug=True)
