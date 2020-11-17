import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
import string
from allData import data_type

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']


@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if BOT_ID != user_id:
        if ' ' in text:
            if BOT_ID != user_id:
                if 'data type' in text:
                    client.chat_postMessage(channel=channel_id,blocks=data_type['dataTypes'])
        elif ' ' not in text:
            if BOT_ID != user_id:
                if text == 'data':
                    client.chat_postMessage(channel=channel_id,blocks=data_type['dataTypes'])

if __name__ == "__main__":
    app.run(debug=True)
    print("Code Ran Perfectly")
