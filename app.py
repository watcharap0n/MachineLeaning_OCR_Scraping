from flask import Flask, request, abort, jsonify, render_template, url_for, redirect
from linebot import LineBotApi, WebhookHandler
import json
import os
import requests
from collections import OrderedDict
import pyrebase
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from random import randrange
from linebot.exceptions import LineBotApiError, InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
from rpa_selenium_scraping import WebScraping
from vision_machine_optical import VisionOCR

app = Flask(__name__)

with open('config/firebase.json', encoding='utf8') as config_file:
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
        events = decoded['events'][i]
        event_handler(events)


def cryptocurrency_scrap():
    my_scrap = WebScraping('config/msedgedriver.exe')
    result = my_scrap.dynamic_scraping(
        uri='https://www.bitkub.com',
        html='table',
        key='class',
        val='deposit__table-wrapper dashboard__table',
        delay=1
    )
    dfs = pd.read_html(str(result))
    data = pd.DataFrame(dfs[0])
    excel = pd.ExcelWriter('static/excel/CryptocurrencyPrices.xlsx', engine='xlsxwriter')
    data.to_excel(excel, sheet_name='Sheet1')
    excel.save()


def event_handle_add():
    raw_json = request.get_json()
    json_line = json.dumps(raw_json)
    decoded = json.loads(json_line)
    return decoded


def get_profile(user_id):
    profile = line_bot_api.get_profile(user_id)
    displayName = profile.display_name
    userId = profile.user_id
    img = profile.picture_url
    status = profile.status_message
    result = {'displayName': displayName, 'userId': userId, 'img': img, 'status': status}
    return result


@app.route('/webhook', methods=['POST'])
def webhook():
    raw_json = request.get_json()
    json_line = json.dumps(raw_json)
    decoded = json.loads(json_line)
    log_line(raw_json)
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    event = decoded['events'][0]
    _type = event['type']
    handler.handle(body, signature)
    try:
        if _type == 'unfollow':
            userId = event['source']['userId']
            remove = db.child('userId_follow').order_by_child('userId').equal_to(userId).get()
            remove = remove.val()
            remove = remove.keys()
            for i in remove:
                db.child('user_follow').child(i).remove()
        elif _type == 'follow':
            userId = event['source']['userId']
            profile = get_profile(userId)
            inserted = {'displayName': profile['displayName'], 'userId': userId, 'img': profile['img'],
                        'status': profile['status']}
            db.child('user_follow').push(inserted)
        elif _type == 'message':
            message_type = event['message']['type']
            if message_type == 'text':
                try:
                    userId = event['source']['userId']
                    message = event['message']['text']
                    profile = get_profile(userId)
                    push_message = {'user_id': userId, 'message': message, 'display_name': profile['displayName'],
                                    'img': profile['img'],
                                    'status': profile['status']}
                    db.child('message_user').push(push_message)
                    handler.handle(body, signature)
                except InvalidSignatureError as v:
                    api_error = {'status_code': v.status_code, 'message': v.message}
                    abort(400)
                    jsonify(api_error)
            else:
                no_event(decoded)
    except LineBotApiError as e:
        abort(400)
        api_error = {'status_code': e.status_code, 'request_id': e.request_id, 'message': e.error.message,
                     'details': e.error.details}
        return jsonify(api_error)
    return jsonify(raw_json)


def event_handler(event):
    _type = event['message']['type']
    if _type == 'sticker':
        sticker_id = randrange(52002734, 52002773)
        reply = event['replyToken']
        sticker_message = StickerSendMessage(
            package_id=str(11537),
            sticker_id=str(sticker_id)
        )
        line_bot_api.reply_message(reply, sticker_message)
    elif _type == 'images':
        img_id = event['message']['id']
        img_id = line_bot_api.get_message_content(img_id)
        with open('static/images/chuck.jpeg', 'wb') as fd:
            for chunk in img_id.iter_content():
                fd.write(chunk)
        replyToken = event['replyToken']
        userId = event['source']['userId']
        message = db.child('message_user').get()
        message_idx = [x.val() for x in message.each() if x.val()['user_id'] == userId]
        if message_idx[-1]['message'] == 'แปลงรูปภาพ':
            ocr = VisionOCR('static/images/chuck.jpeg')
            line_bot_api.reply_message(replyToken, TextSendMessage(text='กรุณารอสักครู่นะค่ะกำลังเข้าสู่กระบวนการ...'))
            text = ocr.document_google()
            line_bot_api.push_message(userId, TextSendMessage(text=text))
        else:
            line_bot_api.reply_message(replyToken, TextMessage(text='รูปสวยดี'))


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    handle = event_handle_add()
    handle = handle['events'][0]
    message = handle['message']['text']
    userId = handle['source']['userId']
    if message == 'แปลงรูปภาพ':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='ทำการใส่รูปมาได้เลยค่ะ...'))
    elif message == 'scraping':
        line_bot_api.reply_message(event.reply_token, TextMessage(text='เรากำลังทำการไปดึงข้อมูล...'))
        cryptocurrency_scrap()
        url = 'https://81f3972b8670.ngrok.io/static/excel/CryptocurrencyPrices.xlsx'
        line_bot_api.push_message(userId, TextMessage(text=url))


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.vue')
    elif request.method == 'POST':
        file_input = request.files['file']
        print(file_input)
        uploads_dir = os.path.join(app.instance_path, 'uploads')
        file_input.save(os.path.join(uploads_dir, file_input.filename))
        ocr = VisionOCR(f'instance/uploads/{file_input.filename}')
        ocr = ocr.document_pandas()
        ocr = ocr.to_dict()
        texts = ocr['description']
        xy = ocr['vertextX']
        range_text = len(texts)
        embedding = []
        for i in range(range_text)[1:]:
            x, y = xy[i]
            embedding.append(y)
        cut_y = list(OrderedDict.fromkeys(embedding).keys())
        results = []
        for i in range(range_text)[1:]:
            x, y = xy[i]
            text = texts[i]
            for e, idx in enumerate(cut_y):
                if idx == y:
                    dic = {e: text}
                    results.append(dic)
        vals = []
        for i in results:
            if i:
                vals.append(i)
        merged = {}
        for k, d in enumerate(vals):
            for j, v in d.items():
                if j not in merged:
                    merged[j] = []
                merged[j].append(v)
        merged['company'] = merged.pop(0)
        merged['tax_id'] = merged.pop(10)
        merged['pos_id'] = merged.pop(13)
        merged['date'] = merged.pop(15)
        merged['list_1'] = merged.pop(21)
        merged['list_2'] = merged.pop(23)
        merged['total_each'] = merged.pop(29)
        merged['pro_1'] = merged.pop(30)
        merged['pro_2'] = merged.pop(31)
        merged['pro_3'] = merged.pop(32)
        merged['price_1'] = merged.pop(33)
        merged['price_2'] = merged.pop(34)
        merged['credit'] = merged.pop(35)
        merged['credit_price'] = merged.pop(36)
        print(merged)
        group = {
            'company': ''.join(merged['company']), 'tax_id': ''.join(merged['tax_id']),
            'pos_id': ''.join(merged['pos_id']), 'date': ''.join(merged['date']),
            'list_1': ''.join(merged['list_1']) + '\n' + ''.join(merged['list_2']) + '\n' + ''.join(
                merged[25]) + ''.join(merged[26]), 'total_each': ''.join(merged['total_each']),
            'pro_1': ''.join(merged['pro_1']) + '  {}'.format(''.join(merged['price_1'])) + '\n' + ''.join(
                merged['pro_2']) + '\n' ''.join(merged['pro_3']) + '  '.join(merged['price_2']),
            'pro_2': ''.join(merged['pro_2']), 'pro_3': ''.join(merged['pro_3']), 'price_1': ''.join(merged['price_1']),
            'price_2': ''.join(merged['price_2']), 'credit': ''.join(merged['credit']),
            'credit_price': ''.join(merged['credit_price'])}
        return jsonify({'form': group, 'texts': texts[0]})


@app.route('/ministry')
def ministry():
    return render_template('ministry.vue')


@app.route('/data_ministry', methods=['POST'])
def data_ministry():
    req = dict(request.get_json())
    keyword = req['keyword']
    revision = req['revision']
    imex_type = req['imex_type']
    order_by = req['order_by']
    url = f"https://dataapi.moc.go.th/products?keyword={keyword}&revision={revision}&imex_type={imex_type}&order_by={order_by}"
    response = requests.get(url, verify=False)
    texts = response.json()
    return jsonify(texts)


@app.route('/bitkub')
def bitkub():
    return render_template('bitkub.vue')


@app.route('/data_bitkub')
def data_bitkub():
    lst = []
    content = WebScraping('config/msedgedriver.exe')
    content = content.dynamic_scraping('https://www.bitkub.com', 'table', 'class',
                                       'deposit__table-wrapper dashboard__table', 1)
    dfs = pd.read_html(str(content))
    dataframe = pd.DataFrame(dfs[0])
    bitkub = dataframe.to_dict()
    bitkub['coin'] = bitkub.pop('สกุลเงิน')
    bitkub['price_last'] = bitkub.pop('ราคาล่าสุด (THB)')
    bitkub['buy_sell'] = bitkub.pop('ซื้อขาย/ วัน')
    bitkub['peak'] = bitkub.pop('สูงสุด/วัน (THB)')
    bitkub['lower'] = bitkub.pop('ต่ำสุด/วัน (THB)')
    coin = bitkub['coin']
    price = bitkub['price_last']
    buy_sell = bitkub['buy_sell']
    peak = bitkub['peak']
    lower = bitkub['lower']
    len_coin = len(coin)
    for i in range(0, len_coin):
        group = {'coin': coin[i], 'price_last': price[i], 'buy_sell': buy_sell[i], 'peak': peak[i], 'lower': lower[i]}
        lst.append(group)
    return jsonify({'bitkub': lst})


@app.route('/dbd')
def dbd():
    return render_template('dbd.vue')


@app.route('/data_dbd', methods=['GET', 'POST'])
def data_dbd():
    if request.method == 'POST':
        try:
            lst = []
            req = request.get_json()
            rpa = WebScraping('config/chromedriver')
            tax_id = req['push_tax']
            url = 'https://datawarehouse.dbd.go.th/'
            content = rpa.dbd_tax(tax_id, url)
            dfs = pd.read_html(str(content))
            dataframe = pd.DataFrame(dfs[0])
            dbd = dataframe.to_dict()
            dbd['index'] = dbd.pop('ลำดับ')
            dbd['tax_id'] = dbd.pop('เลขทะเบียนนิติบุคคล')
            dbd['fname'] = dbd.pop('ชื่อนิติบุคคล')
            dbd['type_person'] = dbd.pop('ประเภทนิติบุคคล')
            dbd['status'] = dbd.pop('สถานะ')
            dbd['bus_id'] = dbd.pop('รหัสประเภทธุรกิจ')
            dbd['bus_name'] = dbd.pop('ชื่อประเภทธุรกิจ')
            dbd['city'] = dbd.pop('จังหวัด')
            dbd['authorized'] = dbd.pop('ทุนจดทะเบียน (บาท)')
            dbd['credit'] = dbd.pop('รายได้รวม (บาท)')
            dbd['profit'] = dbd.pop("กำไร (ขาดทุน) สุทธิ (บาท)")
            dbd['keep_profit'] = dbd.pop('สินทรัพย์รวม (บาท)')
            dbd['prices'] = dbd.pop('ส่วนของผู้ถือหุ้น (บาท)')
            index = dbd['index']
            tax_id = dbd['tax_id']
            fname = dbd['fname']
            type_person = dbd['type_person']
            status = dbd['status']
            bus_id = dbd['bus_id']
            bus_name = dbd['bus_name']
            city = dbd['city']
            authorized = dbd['authorized']
            credit = dbd['credit']
            profit = dbd['profit']
            keep_profit = dbd['keep_profit']
            prices = dbd['prices']
            len_index = len(index)
            for i in range(0, len_index):
                group = {
                    'index': index[i], 'tax_id': tax_id[i], 'fname': fname[i], 'type_person': type_person[i],
                    'status': status[i], 'bus_id': bus_id[i], 'bus_name': bus_name[i], 'city': city[i],
                    'authorized': authorized[i], 'credit': credit[i], 'profit': profit[i],
                    'keep_profit': keep_profit[i], 'prices': prices[i]
                }
                lst.append(group)
            return jsonify({'dbd': lst})
        except NoSuchElementException:
            lst = []
            group = {
                'index': 'Please try again...', 'tax_id': 'Please try again...', 'fname': 'Please try again...',
                'type_person': 'Please try again...',
                'status': 'Please try again...', 'bus_id': 'Please try again...', 'bus_name': 'Please try again...',
                'city': 'Please try again...',
                'authorized': 'Please try again...', 'credit': 'Please try again...', 'profit': 'Please try again...',
                'keep_profit': 'Please try again...', 'prices': 'Please try again...'
            }
            lst.append(group)
            return jsonify({'dbd': lst})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
