import requests
import json
from django.conf import settings

def post_message(channel, text):
    # 본인이 발급받은 토큰값으로 대체
    SLACK_BOT_TOKEN = settings.SLACK_KEY
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + SLACK_BOT_TOKEN
    }
    payload = {
        'channel': channel,
        'text': text
    }
    r = requests.post('https://slack.com/api/chat.postMessage',
                      headers=headers,
                      data=json.dumps(payload)
                      )

