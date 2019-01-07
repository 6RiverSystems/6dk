from flask import jsonify

from app import app
from app.models import Message, Profile
from app.plugins.decipher_engine import decipher


@app.route('/wms/acknowledgement', methods=['POST'])
def receive_acknowledgement():
	payload = request.get_json(force=True) or {}
	logger.debug('receiving pick-waves message: {}'.format(payload))
	token, unmasked_data = decipher(payload, "acknowledgement")
	if token:
		profile = Profile.query.filter_by(token_id=token).first()
		if profile:
			profile = profile.to_dict()
			if profile['data']['northbound_messages']['acknowledgmement']['send']:
				a = 1
				#send northbound
		return
		
		#respond to fs
	else:
		return jsonify({'message': 'accepted but origin wms not found'})


@app.route('/wms/container-accepted', methods=['POST'])
def receive_container_accepted():
	payload = request.get_json(force=True) or {}
	logger.debug('receiving container-accepted message: {}'.format(payload))
	token, unmasked_data = decipher(payload, "container-accepted")
	if token:
		return
		#send northbound
		#respond to fs
	else:
		return jsonify({'message': 'accepted but origin wms not found'})


@app.route('/wms/print-request', methods=['POST'])
def receive_print_request():
	payload = request.get_json(force=True) or {}
	logger.debug('receiving print-request message: {}'.format(payload))
	token, unmasked_data = decipher(payload, "print-request")
	if token:
		return
		#send northbound
		#respond to fs
	else:
		return jsonify({'message': 'accepted but origin wms not found'})


@app.route('/wms/container-validation', methods=['POST'])
def receive_container_validation():
	payload = request.get_json(force=True) or {}
	logger.debug('receiving container-validation message: {}'.format(payload))
	token, unmasked_data = decipher(payload, "container-validation")
	if token:
		return
		#send northbound
		#respond to fs
	else:
		return jsonify({'message': 'accepted but origin wms not found'})


@app.route('/wms/container-inducted', methods=['POST'])
def receive_container_inducted():
	payload = request.get_json(force=True) or {}
	logger.debug('receiving container-inducted message: {}'.format(payload))
	token, unmasked_data = decipher(payload, "container-inducted")
	if token:
		return
		#send northbound
		#respond to fs
	else:
		return jsonify({'message': 'accepted but origin wms not found'})


@app.route('/wms/pick-task-picked', methods=['POST'])
def receive_pick_task_picked():
	payload = request.get_json(force=True) or {}
	logger.debug('receiving pick-task-picked message: {}'.format(payload))
	token, unmasked_data = decipher(payload, "pick-task-picked")
	if token:
		return
		#send northbound
		#respond to fs
	else:
		return jsonify({'message': 'accepted but origin wms not found'})


@app.route('/wms/container-picked-complete', methods=['POST'])
def receive_container_picked_complete():
	payload = request.get_json(force=True) or {}
	logger.debug('receiving container-picked-complete message: {}'.format(payload))
	token, unmasked_data = decipher(payload, "container-picked-complete")
	if token:
		return
		#send northbound
		#respond to fs
	else:
		return jsonify({'message': 'accepted but origin wms not found'})


@app.route('/wms/container-taken-off', methods=['POST'])
def receive_container_taken_off():
	payload = request.get_json(force=True) or {}
	logger.debug('receiving container-taken-off message: {}'.format(payload))
	token, unmasked_data = decipher(payload, "container-taken-off")
	if token:
		return
		#send northbound
		#respond to fs
	else:
		return jsonify({'message': 'accepted but origin wms not found'})