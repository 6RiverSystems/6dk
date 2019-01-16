from datetime import datetime
import json

from flask import flash

from app import db
from app.models import Profile


def check_for_keys(keys, dict):
	missing = [key for key in keys if key not in dict.keys()]
	if len(missing)==0:
		return True, []
	else:
		return False, missing


def first_time_check(key, current_user, flash_desc=True, edit_entry=True):
	try:
		data = current_user.to_dict()['data']
		step = next((step for step in data['startup_steps']
					if step['key']==key), None)
		if step:
			if step['open']:
				step['open'] = False
				step['completed'] = datetime.utcnow().isoformat()+'Z'
				if flash_desc:
					flash(step['description'])
				if edit_entry:
					current_user.data = json.dumps(data)
					db.session.commit()
	except:
		pass


def reset_onboarding(current_user):
	try:
		data = current_user.to_dict()['data']
		for step in data['startup_steps']:
			if step['change_on_reset']:
				step['open'] = True
				current_user.data = json.dumps(data)
				db.session.commit()			
	except:
		pass


def verify_first_pick_wave(token):
	current_user = Profile.find_owner(token)
	if current_user:
		first_time_check('post_pick_wave', current_user, flash_desc=False)
