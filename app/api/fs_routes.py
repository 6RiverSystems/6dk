import json

from flask import request, jsonify

from app import app, db, logger
from app.models import Message
from app.plugins.auth_helper import user_token_validation
from app.plugins.translation_engine import translate
from app.plugins.proxy_helper import mask_proxy


@app.route('/dev/wis-southbound/<version>/pick-waves', methods=['POST'])
@user_token_validation
def receive_pickwaves(version):
	payload = request.get_json(force=True) or {}
	token = request.headers['6Dk-Token']

	#mask data
	masked_data = translate(payload, "pick-waves", token, "mask")

	#save masked and unmasked data
	logger.debug('saving unmasked payload and masked payload')
	message = Message()
	message.from_dict(
						data=dict(
								token_id=token,
								message_type='pick-waves',
								message_format='JSON',
								incoming_endpoint='/dev/wis-southbound/{}/pick-waves'.format(version),
								unmasked_data=json.dumps(payload),
								masked_data=json.dumps(masked_data)
							)
						,
						new_message=True
					)
	db.session.add(message)
	db.session.commit()

	#forward masked data to server
	response = mask_proxy(request, 
						json.dumps(masked_data),
						app.config['DEV_FS_BASE_URL']+'/cfs/wis-southbound/2.3/pick-waves'.format(version))


	#unmask synchronous response from server
	logger.debug('unmasking synchronous response from server')
	unmasked_response = json.dumps(
							translate(
										response.get_json(), 
										"pick-waves-response", 
										token,
										"unmask"
										))

	#save masked and unmasked synchronous response fron server
	logger.debug('saving unmasked response and masked response')
	message = Message()
	message.from_dict(
						data=dict(
								token_id=token,
								message_type='pick-waves-response',
								message_format='JSON',
								incoming_endpoint='/dev/wis-southbound/{}/pick-waves'.format(version),
								unmasked_data=unmasked_response,
								masked_data=json.dumps(response.get_json())
							)
						,
						new_message=True
					)
	db.session.add(message)
	db.session.commit()
	response.data = unmasked_response
	return response



@app.route('/exp/wis-southbound/<version>/pick-waves', methods=['POST'])
@user_token_validation
def receive_exception_pickwaves(version):
	#check auth
	#mask fields
	#save to database
	return "foo bar bazz"


@app.route('/exp/wis-order-update/<version>/group-updates', methods=['POST'])
@user_token_validation
def receive_group_updates(version):
	#check auth
	#mask fields
	#save to database
	return


@app.route('/exp/wis-order-update/<version>/group-cancels', methods=['POST'])
@user_token_validation
def receive_group_cancels(version):
	#check auth
	#mask fields
	#save to database
	return