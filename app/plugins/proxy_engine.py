import json

from app import app, db, logger
from app.models import Message
from app.plugins.proxy.proxy_helper import _proxy
from app.plugins.translation_engine import translate


def save_message(data, masked_data, message_type, incoming_endpoint, token,
					message_format='JSON'):
	logger.debug('saving unmasked data and masked data for {} message'.format(
																message_type))
	message = Message()
	message.from_dict(
						data=dict(
								token_id=token,
								message_type=message_type,
								message_format=message_format,
								incoming_endpoint=incoming_endpoint,
								unmasked_data=json.dumps(data),
								masked_data=json.dumps(masked_data)
							)
						,
						new_message=True
					)
	db.session.add(message)
	db.session.commit()



def serve_proxy(data, masked_data, message_type, incoming_endpoint, token, 
				destination):
	save_message(data, masked_data, message_type, incoming_endpoint, token)
	response = _proxy(request, json.dumps(masked_data), destination)
	response_message_type = message_type + '-response'
	logger.debug('unmasking synchronous {} from server'.format(
														response_message_type))
	unmasked_response = json.dumps(translate(response.get_json(), 
										response_message_type, token, "unmask"))
	save_message(unmasked_response, response.get_json(), response_message_type,
				incoming_endpoint, token)
	response.data = unmasked_response
	return response