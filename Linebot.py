# Running in Google Cloud Function

import os, json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests

def main(request):
    body = request.get_data(as_text=True)                    
    try:
        json_data = json.loads(body)                         
        access_token = os.environ.get('LineToken', 'token')
        secret = os.environ.get('LineSecret', 'Secret')
        line_bot_api = LineBotApi(access_token)              
        handler = WebhookHandler(secret)             
        print('handler established')        
        signature = request.headers['X-Line-Signature']     
        print(request.headers['X-Line-Signature']) 
        handler.handle(body, signature)                      
        msg = json_data['events'][0]['message']['text']      
        tk = json_data['events'][0]['replyToken']    
        
        ai_Key = os.environ.get('OpenAIKey','ChatGPT')
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": msg}],
        }
        headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer "+ ai_Key
        }
        print(payload)
        print(headers)

        response = requests.post("https://api.openai.com/v1/chat/completions",json=payload,headers=headers)    
        reply = response.json()

        line_bot_api.reply_message(tk,TextSendMessage(reply['choices'][0]['message']['content']))  
        print(msg, tk)                                       
    except:
        print(body)                                          
    return 'OK'  
