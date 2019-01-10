import json
from datetime import datetime
from flask import jsonify

from app import db, logger
import copy

from app.models import Message, MessageTransmission, Profile
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
	transmission = MessageTransmission()
	transmission.from_dict(
						data=dict(
								message_id=message.id
							)
						,
						new_transmission=True
					)
	db.session.add(transmission)
	db.session.commit()


def serve_proxy(data, masked_data, message_type, incoming_endpoint, token, 
				destination, request):
	save_message(data, masked_data, message_type, incoming_endpoint, token)
	response = _proxy(request, json.dumps(masked_data), destination)
	response_message_type = message_type + '-response'
	logger.debug('unmasking synchronous {} from server'.format(
														response_message_type))
	original_response = response.get_json(force=True) or {}
	copied_response = copy.deepcopy(original_response)
	unmasked_response = translate(copied_response, response_message_type, token, 
									"unmask")
	save_message(unmasked_response, original_response, response_message_type,
				incoming_endpoint, token)
	response.data = json.dumps(unmasked_response)
	return response


def wms_forwarder(data, masked_data, message_type, incoming_endpoint, token, 
				request):
	save_message(data, masked_data, message_type, incoming_endpoint, token)
	profile = Profile.query.filter_by(token_id=token).first()
	if profile:
		profile = profile.to_dict()
		message_settings = next(
								(msg 
								for msg in profile['data']['northbound_messages']
								if msg['name'] == message_type
								), None)
		if message_settings:
			if message_settings['send']:
				destination = message_settings['wms_host'] \
							+ ':' + str(message_settings['wms_port']) \
							+ '/' + message_settings['wms_path']
				for header in message_settings:
					request.headers.append({
											header.split(':')[0]: header.split(':')[-1]
											})
				response = _proxy(request, json.dumps(masked_data), destination)
				response_message_type = message_type + '-response'
				try:
					save_message(response.get_json(), response.get_json(), 
								response_message_type, incoming_endpoint, token)
				except:
					logger.debug('could not save {}'.format(response_message_type))
				return response
			else:
				return jsonify({'msg': 'accepted but not forwarding to wms'})
		else:
			return jsonify({'msg': 'accepted but {} message settings not found'.format(message_type)})
	else:
		return jsonify({'msg': 'accepted but profile not found'})



def wms_repeater(message_id):
	transmission = MessageTransmission()
	transmission.from_dict(
						data=dict(
								message_id=message_id
							)
						,
						new_transmission=True
					)
	message = Message.query.filter_by(id=message_id).first()
	message.updated = datetime.utcnow()
	db.session.add(transmission)
	db.session.commit()