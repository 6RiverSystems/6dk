import json
from datetime import datetime
from uuid import uuid4
from time import time

import jwt
from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db, login


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, table, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, table=table,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, table=table,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, table=table,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


@login.user_loader
def load_user(id):
    return User.query.get(id)


class User(UserMixin, db.Model):
	id = db.Column(db.String(128), index=True, unique=True, primary_key=True)
	email = db.Column(db.String(128), index=True, unique=True)
	first_name = db.Column(db.String(128))
	last_name = db.Column(db.String(128))
	data = db.Column(db.String(16777216), default="{}")
	password_hash = db.Column(db.String(128))
	active_profile = db.Column(db.String(128), db.ForeignKey('profile.token_id'))
	deleted = db.Column(db.Boolean(), default=False)
	last_feed_load_time = db.Column(db.DateTime())
	created = db.Column(db.DateTime(), default=datetime.utcnow)
	updated = db.Column(db.DateTime(), default=datetime.utcnow)

	def __repr__(self):
		return '<User {}>'.format(self.email)    

	def to_dict(self):
		data = {
			'id': self.id,
			'email': self.email,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'created': self.created.isoformat()+'Z',
			'updated': self.updated.isoformat()+'Z',
		}
		try:
			data['data'] = json.loads(self.data)
		except:
			data['data'] = {}
		return data

	def from_dict(self, data, new_user=False):
		for field in ['email', 'first_name', 'last_name']:
			if field in data:
				setattr(self, field, data[field])
		if new_user:
				setattr(self, 'id', str(uuid4()))
		else:
				self.updated = datetime.utcnow()

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
		self.updated = datetime.utcnow()

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def load_user_profiles(self, deleted=False):
		profiles = [profile.to_dict() 
					for profile in
					Profile.query.filter_by(user=self.id,
											deleted=deleted).all()]
		profiles = sorted(profiles, key=lambda x: x['data']['friendly_name'])
		return profiles

	def get_active_profile(self):
		profile = Profile.query.filter_by(token_id=self.active_profile).first()
		if profile:
			return profile.to_dict()
		else:
			return None

	def owns_token(self, token):
		token = Profile.query.filter_by(token_id=token, user=self.id).first()
		if token:
			return True
		else:
			return False

	def new_messages(self):
		last_load_time = self.last_feed_load_time or datetime(2000,1,1)
		token_ids = [profile['token_id'] for profile in self.load_user_profiles()]
		return Message.query.filter(Message.token_id.in_(token_ids), 
					Message.created > last_load_time).count()


	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
					{'reset_password': self.id, 'exp': time() + expires_in},
					app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, app.config['SECRET_KEY'],
			algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)

	def get_forward_profile_token(self, destination, profile_token, expires_in=600):
		return jwt.encode(
							{
							'source': self.id,
							'destination': destination.id,
							'profile': profile_token,
							'exp': time() + expires_in
							},
						app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	def receive_forward_profile_token(self, jwt_token):
		try:
			token_data = jwt.decode(jwt_token, app.config['SECRET_KEY'],
			algorithms=['HS256'])
			if token_data['destination'] == self.id \
					and User.query.get(token_data['source']).owns_token(token_data['profile']) \
					and Profile.is_active(token_data['profile']) \
					and not self.owns_token(token_data['profile']):
				return token_data
		except:
			return


class Profile(PaginatedAPIMixin, db.Model):
	token_id = db.Column(db.String(128), index=True, unique=True, primary_key=True)
	user  = db.Column(db.String(128), db.ForeignKey('user.id'))
	data = db.Column(db.String(16777216), default="{}")
	deleted = db.Column(db.Boolean(), default=False)
	created = db.Column(db.DateTime(), default=datetime.utcnow)
	updated = db.Column(db.DateTime(), default=datetime.utcnow)
    
	def __repr__(self):
		return '<Token {}>'.format(self.token_id)

	def to_dict(self):
		data = {
			'token_id': self.token_id,
			'user': self.user,
			'created': self.created.isoformat()+'Z',
			'updated': self.updated.isoformat()+'Z',
		}
		try:
			data['data'] = json.loads(self.data)
		except:
			data['data'] = {}
		return data

	def from_dict(self, data, new_profile=False):
		for field in ['user', 'data']:
			if field in data:
				setattr(self, field, data[field])
		if new_profile:
				setattr(self, 'token_id', str(uuid4()))
		else:
			self.updated = datetime.utcnow()

	def is_active(token):
		profile = Profile.query.filter_by(token_id=token).first()
		if profile:
			if profile.deleted:
				return False
			else:
				return True
		else:
			return False


class MaskMap(PaginatedAPIMixin, db.Model):
	value = db.Column(db.String(128), index=True, unique=True, primary_key=True)
	token_id = db.Column(db.String(128), db.ForeignKey('profile.token_id'))
	field_name = db.Column(db.String(128))
	external_value = db.Column(db.String(2048))
	created = db.Column(db.DateTime(), default=datetime.utcnow)
	updated = db.Column(db.DateTime(), default=datetime.utcnow)

	def __repr__(self):
		return '<MaskMap {}>'.format(self.value)

	def to_dict(self):
		data = {
			'value': self.value,
			'token_id': self.token_id,
			'field_name':self.field_name,
			'external_value': self.external_value,
			'created': self.created.isoformat()+'Z',
			'updated': self.updated.isoformat()+'Z',
		}
		return data

	def from_dict(self, data, new_mask_map=False):
		for field in ['value', 'token_id', 'field_name', 'external_value']:
			if field in data:
				setattr(self, field, data[field])
		if not new_mask_map:
			self.updated = datetime.utcnow()


class Message(PaginatedAPIMixin, db.Model):
	id = db.Column(db.String(128), index=True, unique=True, primary_key=True)
	token_id = db.Column(db.String(128), db.ForeignKey('profile.token_id'))
	message_type = db.Column(db.String(128))
	message_format = db.Column(db.String(128))
	incoming_endpoint = db.Column(db.String(2048))
	unmasked_data = db.Column(db.String(16777216))
	masked_data = db.Column(db.String(16777216))
	created = db.Column(db.DateTime(), default=datetime.utcnow)
	updated = db.Column(db.DateTime(), default=datetime.utcnow)

	def __repr__(self):
		return '<Message {}>'.format(self.id)

	def to_dict(self, include_profile=False, parse_timestamps=False,
				include_transmissions=False):
		data = {
			'id': self.id,
			'token_id': self.token_id,
			'message_type': self.message_type,
			'message_format': self.message_format,
			'incoming_endpoint': self.incoming_endpoint,
			'unmasked_data': self.unmasked_data,
			'masked_data': self.masked_data,
		}
		if include_profile:
			data['profile'] = Profile.query.filter_by(token_id=self.token_id
        											).first().to_dict()
		if parse_timestamps:
			data['created'] = self.created
			data['updated'] = self.updated
		else:
			data['created'] = self.created.isoformat()+'Z'
			data['updated'] = self.updated.isoformat()+'Z'

		if include_transmissions:
			data['transmissions_info'] = Message.get_replays(self.id)
		return data

	def from_dict(self, data, new_message=False):
		for field in ['token_id', 'message_type', 'message_format',
						'incoming_endpoint', 'unmasked_data', 'masked_data']:
			if field in data:
				setattr(self, field, data[field])
		if new_message:
				setattr(self, 'id', str(uuid4()))
		else:
			self.updated = datetime.utcnow()

	def get_replays(message_id):
		transmissions = MessageTransmission.query.filter_by(message_id=message_id
								).order_by(MessageTransmission.updated.asc()).all()
		data = {'count': len(transmissions)}
		data['transmissions'] = [transmission.to_dict(parse_timestamps=True) 
								for transmission in transmissions]
		return data


class MessageTransmission(PaginatedAPIMixin, db.Model):
	id = db.Column(db.String(128), index=True, unique=True, primary_key=True)
	message_id = db.Column(db.String(128), db.ForeignKey('message.id'))
	created = db.Column(db.DateTime(), default=datetime.utcnow)
	updated = db.Column(db.DateTime(), default=datetime.utcnow)

	def __repr__(self):
		return '<MessageTransmission {}>'.format(self.id)

	def to_dict(self, include_profile=False, parse_timestamps=False):
		data = {
			'id': self.id,
			'message_id': self.message_id
		}
		if include_profile:
			data['profile'] = Profile.query.filter_by(token_id=self.token_id
        											).first().to_dict()
		if parse_timestamps:
			data['created'] = self.created
			data['updated'] = self.updated
		else:
			data['created'] = self.created.isoformat()+'Z'
			data['updated'] = self.updated.isoformat()+'Z'
		return data


	def from_dict(self, data, new_transmission=False):
		for field in ['message_id']:
			if field in data:
				setattr(self, field, data[field])
		if new_transmission:
				setattr(self, 'id', str(uuid4()))
		else:
			self.updated = datetime.utcnow()