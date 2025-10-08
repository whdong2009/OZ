from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

app = Flask(__name__)

# 設定 LINE Bot
configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


# Webhook 接收路徑
@app.route("/callback", methods=['POST'])
def callback():
    # 取得 X-Line-Signature header
    signature = request.headers['X-Line-Signature']

    # 取得請求內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 驗證簽章
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 處理文字訊息
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # 取得用戶傳送的訊息
    user_message = event.message.text

    # 基礎回覆邏輯
    if user_message == "你好":
        reply_text = "您好!歡迎來到立炘室內設計VIP會客室\n我可以協助您:\n1. 預約諮詢\n2. 查看作品集\n3. 了解服務項目\n\n請輸入數字選擇服務"

    elif user_message == "1":
        reply_text = "預約諮詢服務\n\n請問您的房屋類型是?\n1. 新成屋\n2. 中古屋\n3. 商業空間"

    elif user_message == "2":
        reply_text = "作品集展示\n\n您可以前往我們的官網查看:\nhttps://www.example.com/portfolio"

    elif user_message == "3":
        reply_text = "服務項目:\n✓ 室內設計規劃\n✓ 裝潢工程施工\n✓ 軟裝搭配建議\n✓ 3D 設計圖製作"

    else:
        reply_text = f"您說: {user_message}\n\n請輸入「你好」開始對話"

    # 回覆訊息
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )


# 測試用路徑
@app.route("/")
def home():
    return "LINE Bot is running!"


if __name__ == "__main__":
    # 本地測試時使用
    app.run(debug=True, port=5000)