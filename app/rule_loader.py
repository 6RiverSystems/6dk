import json
from uuid import uuid4

import requests


class Rule():
	def __init__(self, rules_dictionary, app_config):
		self.rules_dictionary = rules_dictionary
		self.app_config = app_config


	def substitutes(self, message_type, message_format='JSON'):
		message = next((rule for rule in self.rules_dictionary['messages']
						if rule['message_type']==message_type
						and rule['message_format']==message_format), None)
		if message:
			if 'substitute_paths' in message.keys():
				return message['substitute_paths']
			else:
				return
		else:
			return


	def sanitizers(self, message_type, message_format='JSON'):
		message = next((rule for rule in self.rules_dictionary['messages']
						if rule['message_type']==message_type
						and rule['message_format']==message_format), None)
		if message:
			print('found message')
			if 'sanitize_paths' in message.keys():
				return message['sanitize_paths']
			else:
				return
		else:
			print('did not find message')
			return


	def sanitize_value(self, message_type, field_name, 
						message_format='JSON'):
		print('sanitizing '+ field_name)
		message = next((rule for rule in self.rules_dictionary['messages']
						if rule['message_type']==message_type
						and rule['message_format']==message_format), None)
		if message:
			print('found message')
			sanitizer_name = next((rule['sanitizer'] for rule in message['sanitize_paths']
							if rule['field_name']==field_name), None)
		else:
			print('did not find message')
			sanitizer_name = None

		if sanitizer_name:
			print('found sanitizer name')
			sanitizer = next((rule for rule in self.rules_dictionary['sanitizers']
						if rule['name']==sanitizer_name), None)

		else:
			print('did not find sanitizer name')
			sanitizer = None

		if sanitizer:
			print('found sanitizer')
			return self.stub_element(sanitizer)
		else:
			print('did not find sanitizer')
			return None


	def stub_element(self, sanitizer):
		new_id = str(uuid4())
		payload = dict(sanitizer['creation_body'])
		to_replace = [key for key in payload.keys() if payload[key]=='*']
		for key in to_replace:
			payload[key] = new_id
		print(json.dumps(payload))
		r = requests.post(
							self.app_config['DEV_FS_BASE_URL']+sanitizer['creation_url'],
							data=json.dumps(payload), 
							timeout=2
							)
		print(r.json())
		return new_id