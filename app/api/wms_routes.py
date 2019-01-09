import copy

from flask import jsonify, request

from app import app, logger, rule
from app.plugins.decipher_engine import decipher
from app.plugins.proxy_engine import wms_forwarder


@app.route('/wms/<message_type>', methods=['POST'])
def receive_wms_request(message_type):
	valid_messages = rule.get_northbound_messages()
	if message_type in valid_messages:
		original_payload = request.get_json(force=True) or {}
		payload = copy.deepcopy(original_payload)
		logger.debug('receiving {0} message: {1}'.format(message_type, payload))
		token, unmasked_data = decipher(payload, message_type)
		if token:
			return wms_forwarder(unmasked_data, original_payload, message_type, 
						'/wms/{}'.format(message_type), token, 
						request)
		else:
			return jsonify({'message': 'accepted but origin wms not found'})	
	else:
		return jsonify({'message': 'unknown message type'}), 404