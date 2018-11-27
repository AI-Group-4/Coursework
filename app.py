import os,sys
from flask import Flask, request
from readWit import wit_response,get_news_elements
import requests




app = Flask(__name__)
PAGE_ACCESS_TOKEN_1 = 'EAAf8lGp4TlIBAGo8NVIe4KvecFZCFxI0LXhZAydXZBDCcy7N0veEZBhQu3sMDetSYlGSYSXZCPRZAZAOFsHQnkjENpiYX5ZChMmGvqApZAL83NR0xZCffjw9iru2I2jHfaNUT9hxZCEZCjzKIBexZAxxDhUwQy7X1q38WZBZBDG8JXOXuUl6gZDZD'
VERIFICATION_TOKEN = "helloRailinformation"


@app.route('/', methods=['GET'])
def verify():
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Hello new world", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data['object']=='page':
        for entry in data['entry']:
            my_id = entry['id']
            for msging_event in entry['messaging']:
                print(msging_event)
                s_id = msging_event['sender']['id']
                if msging_event.get('message'):
                    if 'text' in msging_event['message']:
                        msg_text = msging_event['message']['text']
                        print('111111111')
                        print(msg_text)
                        newRply = get_news_elements(wit_response(msg_text,s_id),s_id,msg_text)
                    else:
                        msg_text = 'no text'
                    reply(s_id,newRply)
  
    return "ok",200


def log(message):
    print(message)
    
    sys.stdout.flush()

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + PAGE_ACCESS_TOKEN_1, json=data)

if __name__ == "__main__":
	app.run(debug =True,port=3000)