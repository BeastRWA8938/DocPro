import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
import string

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']



data_type = {	
    "dataTypes": [{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Here is some info on Data Types,"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*String*\n Every thing that we write in quots is concidered as a String."
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Integer*\n All the numbers from -infinity to +infinity are Integers."
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Float*\n All the numbers containing Deciamls are Float."
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*List*\n Every thing in Square Brackets seperating with comma is a List."
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Tuple*\n Every thing in Curve Brackets seperating with comma is a Tuple."
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Dictionary*\n Every thing in curly brackets and data seperated in key value pairs is a Dictionary"
			}
		}]
}



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
