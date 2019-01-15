import copy
from flask import request,jsonify

from app import app, logger
from app.plugins.auth_helper import user_token_validation
from app.plugins.translation_engine import translate
from app.plugins.proxy_engine import serve_proxy


@app.route('/<mode>/wis-southbound/<version>/pick-waves', methods=['POST'])
@user_token_validation
def receive_pickwaves(mode, version):
	original_payload = request.get_json(force=True) or {}
	payload = copy.deepcopy(original_payload)
	logger.debug('receiving pick-waves message: {}'.format(payload))
	token = request.headers['6Dk-Token']
	#mask data
	if mode=='dev':
		masked_data = translate(payload, 'pick-waves', token, 'mask')
	elif mode=='exp':
		masked_data = translate(payload, 'pick-waves', token, 'mask', 
								exception=True)
	else:
		return jsonify({'message': 'bad request'}), 400
	response = serve_proxy(original_payload, masked_data, 'pick-waves', 
						'/dev/wis-southbound/{}/pick-waves'.format(version),
						token, app.config['DEV_FS_BASE_URL'] + \
						'/cfs/wis-southbound/2.3/pick-waves'.format(version),
						request)
	return response


@app.route('/dev/wis-order-update/<version>/group-updates', methods=['POST'])
@user_token_validation
def receive_group_updates(version):
	#check auth
	#mask fields
	#save to database
	return


@app.route('/dev/wis-order-update/<version>/group-cancels', methods=['POST'])
@user_token_validation
def receive_group_cancels(version):
	#check auth
	#mask fields
	#save to database
	return


