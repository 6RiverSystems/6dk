from flask import jsonify

from app import db, logger
from app.models import User


def create_new_user(data):
	logger.debug('creating new user')
	exist = User.query.filter_by(email=data['email']).first()
	if not exist:
		user = User()
		user.from_dict(data, new_user=True)
		print(user)
		user.set_password(data['password'])
		print(user)
		db.session.add(user)
		db.session.commit()
		print(user, user.to_dict())
		logger.debug('created new user for: {}'.format(data['email']))
		return jsonify(user.to_dict()), True
	else:
		return jsonify({
						'message': 'User for email, {}, already exists'.format(
																data['email'])
						}), False