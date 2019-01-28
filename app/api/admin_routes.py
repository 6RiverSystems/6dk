import json
import string
import random

from flask import request, jsonify

from app import app, db, logger
from app.models import Profile, User
from app.plugins.auth_helper import admin_token_validation
from app.plugins.general_helper import check_for_keys
from app.plugins.profile_helper import create_new_profile
from app.plugins.user_helper import create_new_user
from app.plugins.mail_helper import send_welcome


@app.route('/admin/users', methods=['GET', 'POST'])
@admin_token_validation
def create_user():
	if request.method=='POST':
		data = request.get_json(force=True) or {}
		logger.debug('receiving request to add user: {}'.format(data))
		welcome = request.args.get('welcome', 0, type=int)
		if welcome:
			temp_pass = ''.join(
						random.choice(string.ascii_uppercase + string.digits \
										+string.ascii_lowercase) 
						for _ in range(12))
			data['password'] = temp_pass
		all_keys_present, results = check_for_keys(['email', 'first_name', 
													'last_name', 'password'], data)
		if all_keys_present:
			logger.debug('adding user {}'.format(data['email']))
			response, success = create_new_user(data)
			if success:
				logger.debug('added user {}'.format(data['email']))
				user = User.query.filter_by(email=data['email']).first()
				if welcome:
					send_welcome(user, temp_pass)
				response.status_code = 201
			else:
				logger.debug('failed to add {}'.format(data['email']))
				response.status_code = 400
			return response
		else:
			logger.debug('missing {}'.format(', '.join(results)))	
			return jsonify({'message': 'missing {}'.format(', '.join(results)) }), 400
	else:
		return query_users(request)


def query_users(request):
	user_id = request.args.get('id')
	user_email = request.args.get('email')

	if user_id or user_email:
		search = True
	else:
		search = False

	if search:
		if user_id:
			user = User.query.filter_by(id=user_id).first()
		elif user_email:
			user = User.query.filter_by(email=user_email).first()
		if user:
			return jsonify(user.to_dict())
		else:
			return jsonify({'msg': 'user not found'}), 404
	else:
		page = request.args.get('page', 1, type=int)
		per_page = app.config['ELEMENTS_PER_PAGE']
		data = User.to_collection_dict(
										User.query, 
										page, 
										per_page, 
										'create_user', 
										'User'
										)
		return jsonify(data)



@app.route('/admin/profiles', methods=['POST', 'GET'])
@admin_token_validation
def create_profile():
	if request.method=='POST':
		data = request.get_json(force=True) or {}
		all_keys_present, results = check_for_keys(['email'], data)
		if all_keys_present:
			user = User.query.filter_by(email=data['email']).first()
			if user:
				data['user'] = user.id
				profile = create_new_profile(data)
				response = jsonify(profile)
				response.status_code = 201
				return response
			return jsonify({'message': 'user not found for email: {}'.format(data['email'])}), 400
		else:		
			return jsonify({'message': 'missing {}'.format(', '.join(results)) }), 400
	else:
		return query_profiles(request)


def query_profiles(request):
	token = request.args.get('token')
	if token:
		profile = Profile.query.filter_by(token_id=token).first()
		if profile:
			return jsonify(profile.to_dict())
		else:
			return jsonify({'msg': 'profile not found'}), 404
	else:
		page = request.args.get('page', 1, type=int)
		per_page = app.config['ELEMENTS_PER_PAGE']
		data = User.to_collection_dict(
										Profile.query, 
										page, 
										per_page, 
										'create_profile', 
										'Profile'
										)
		return jsonify(data)


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
			db.session.commit()
			return jsonify(profile.to_dict())
	else:
		return jsonify({'message': 'missing {}'.format(', '.join(results)) }), 400


def delete_profile(token_id, data, profile):
	logger.debug('deleting profile: {}'.format(profile.token_id))
	profile.deleted = True
	db.session.commit()
	response = jsonify({'message': 'profile deleted'})
	response.status_code = 202
	return response