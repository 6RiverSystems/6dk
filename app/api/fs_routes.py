import json

from flask import request, jsonify

from app import app, db, logger
from app.models import Message
from app.plugins.auth_helper import user_token_validation
from app.plugins.mask_engine import mask_payload_fields


@app.route('/dev/wis-southbound/<version>/pick-waves', methods=['POST'])
@user_token_validation
def receive_pickwaves(version):
	payload = request.get_json(force=True) or {}
	masked_data = mask_payload_fields(payload, 
								"pickWaves", 
								request.headers['6Dk-Token'])
	logger.debug('saving payload and masked payload')
	message = Message()
	message.from_dict(
						data=dict(
								token_id=request.headers['6Dk-Token'],
								message_type='pickWaves',
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
	#response = _proxy(request, app.config['DEV_FS_BASE_URL']+'/cfs/wis-southbound/{}/pick-waves'.format(version))
	#logger.debug('unmasking synchronous response from server')
	#response.content = json.dumps({'foo':'bar'})
	return jsonify(masked_data)#response



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