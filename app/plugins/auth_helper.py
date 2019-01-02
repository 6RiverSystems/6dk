from functools import wraps

from flask import request, jsonify

from app import app, logger
from app.models import Profile


def user_token_validation(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		headers = request.headers
		logger.debug('checking 6Dk-Token')
		if '6Dk-Token' in headers.keys():
			profile = Profile.query.filter_by(
									token_id=headers['6Dk-Token']).first()
			if profile != None:
				logger.debug('6Dk-Token accepted')
				return f(*args, **kwargs)
			else:
				logger.debug('6Dk-Token not found')
				return jsonify({'message': '6Dk-Token not found'}), 401
		else:
			logger.debug('no 6Dk-Token supplied')
			return jsonify({'message': 'no 6Dk-Token supplied'}), 401
	return decorated_function


def admin_token_validation(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		headers = request.headers
		logger.debug('checking 6Dk-Admin-Token')
		if '6Dk-Admin-Token' in headers.keys():
			if headers['6Dk-Admin-Token'] in app.config['ADMIN_TOKENS']:
				logger.debug('6Dk-Admin-Token accepted: {}'.format(
													headers['6Dk-Admin-Token'])
													)
				return f(*args, **kwargs)
			else:
				logger.debug('6Dk-Admin-Token not found')
				return jsonify({'message': '6Dk-Admin-Token not found'}), 401
		else:
			logger.debug('no 6Dk-Admin-Token supplied')
			return jsonify({'message': 'no 6Dk-Admin-Token supplied'}), 401
	return decorated_function