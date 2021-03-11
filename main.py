# %%
import json
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv
load_dotenv()
# %%
url = 'https://backend.dr-plano.de/courses_dates?id=67152448&start=1614553200000&end=1617228000000'

res = requests.get(url)
slots = json.loads(res.text)

df = pd.DataFrame(slots)

# %%
unavailable_states = ['NOT_BOOKABLE_ANYMORE', 'FULLY_BOOKED', 'NOT_YET_BOOKABLE']
# unavailable_states = ['FULLY_BOOKED', 'NOT_BOOKABLE_ANYMORE']

def is_available(state: str):
	if state in unavailable_states:
		return False
	return True

def unix_to_datetime(ts):
	return datetime.fromtimestamp(int(ts) / 1000)

def pushbullet_message(title, body):
	msg = {"type": "note", "title": title, "body": body}
	TOKEN = os.getenv('PUSHBULLET_TOKEN') 
	resp = requests.post('https://api.pushbullet.com/v2/pushes', 
												data=json.dumps(msg),
												headers={'Authorization': 'Bearer ' + TOKEN,
																 'Content-Type': 'application/json'})
	if resp.status_code != 200:
		print(resp.headers)
		raise Exception('Error',resp.status_code)
		

# %%
filt = df['state'].apply(is_available)
available = df[filt]
if len(available) > 5:
	pushbullet_message('Many new slots available.', len(available))
else:
	for index, slot in available.iterrows():
		slot_time = unix_to_datetime(slot['dateList'][0]['start'])
		available_slots = int(slot['maxCourseParticipantCount']) - int(slot['currentCourseParticipantCount'])
		pushbullet_message(str(slot_time), f'Available Slots: {available_slots}')
		# print(index)
		# if index == 155:
		# 	break