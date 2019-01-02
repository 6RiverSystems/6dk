import json

from flask import request, jsonify

from app import app, db, logger
from app.models import Profile, MaskPath
from app.plugins.auth_helper import admin_token_validation
from app.plugins.general_helper import check_for_keys


@app.route('/admin/profiles', methods=['POST'])
@admin_token_validation
def create_profile():
	data = request.get_json(force=True) or {}
	all_keys_present, results = check_for_keys(['email'], data)
	if all_keys_present:
		logger.debug('creating new profile')
		profile = Profile()
		profile.from_dict(data, new_profile=True)
		db.session.add(profile)
		db.session.commit()
		response = jsonify(profile.to_dict())
		response.status_code = 201
		return response
	else:		
		return jsonify({'message': 'missing {}'.format(', '.join(results)) }), 400



@app.route('/admin/profiles/<token_id>', methods=['PUT', 'DELETE'])
@admin_token_validation
def mod_profile(token_id):
	data = request.get_json(force=True) or {}
	profile = Profile.query.filter_by(token_id=token_id).first()
	if profile == None:
		return jsonify({'message': 'profile not found'}), 404
	if request.method=='PUT':
		return edit_profile_data(token_id, data, profile)
	elif request.method=='DELETE':
		return delete_profile(token_id, data, profile)



def edit_profile_data(token_id, data, profile):
	all_keys_present, results = check_for_keys(['data'], data)
	if all_keys_present:
		if not isinstance(data['data'], dict):
			return jsonify({'message': 'data must be an object'}), 400
		else:
			logger.debug('updating data')
			profile.from_dict({'data': json.dumps(data['data'])})
			return jsonify(profile.to_dict())
	else:
		return jsonify({'message': 'missing {}'.format(', '.join(results)) }), 400



def delete_profile(token_id, data, profile):
	logger.debug('deleting profile: {}'.format(profile.token_id))
	db.session.delete(profile)
	db.session.commit()
	response = jsonify({'message': 'profile deleted'})
	response.status_code = 202
	return response


@app.route('/admin/mask-paths', methods=['POST'])
@admin_token_validation
def create_mask_path():
	data = request.get_json(force=True) or {}
	all_keys_present, results = check_for_keys(
												[
													'message_type', 
													'key_path', 
													'field_name', 
													'message_format', 
												], 
												data)
	if all_keys_present:
		logger.debug('creating new mask path')
		profile = MaskPath()
		profile.from_dict(data, new_mask_path=True)
		db.session.add(profile)
		db.session.commit()
		response = jsonify(profile.to_dict())
		response.status_code = 201
		return response
	else:
		return jsonify({'message': 'missing {}'.format(', '.join(results)) }), 400


