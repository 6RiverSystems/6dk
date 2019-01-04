import json
from datetime import datetime
from uuid import uuid4

from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


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
	password_hash = db.Column(db.String(128))
	created = db.Column(db.DateTime(), default=datetime.utcnow)
	updated = db.Column(db.DateTime(), default=datetime.utcnow)

	def __repr__(self):
		return '<User {}>'.format(self.email)    

	def to_dict(self):
		data = {
			'email': self.email,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'created': self.created.isoformat()+'Z',
			'updated': self.updated.isoformat()+'Z',
		}

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


class Profile(PaginatedAPIMixin, db.Model):
	token_id = db.Column(db.String(128), index=True, unique=True, primary_key=True)
	email  = db.Column(db.String(128), db.ForeignKey('user.email'))
	data = db.Column(db.String(16777216), default="{}")
	created = db.Column(db.DateTime(), default=datetime.utcnow)
	updated = db.Column(db.DateTime(), default=datetime.utcnow)
    
	def __repr__(self):
		return '<Token {}>'.format(self.token_id)

	def to_dict(self):
		data = {
            'token_id': self.token_id,
            'email': self.email,
            'data': json.loads(self.data),
            'created': self.created.isoformat()+'Z',
            'updated': self.updated.isoformat()+'Z',
        }
		return data

	def from_dict(self, data, new_profile=False):
		for field in ['email', 'data']:
			if field in data:
				setattr(self, field, data[field])
		if new_profile:
				setattr(self, 'token_id', str(uuid4()))
		else:
			self.updated = datetime.utcnow()


class MaskMap(PaginatedAPIMixin, db.Model):
	value = db.Column(db.String(128), index=True, unique=True, primary_key=True)
	token_id = db.Column(db.String(128), db.ForeignKey('profile.token_id'))
	field_name = db.Column(db.String(128))
	external_value = db.Column(db.String(2048))
	created = db.Column(db.DateTime(), default=datetime.utcnow)
	updated = db.Column(db.DateTime(), default=datetime.utcnow)

	def __repr__(self):
		return '<MaskMap {}>'.format(self.id)

	def to_dict(self):
		data = {
            'id': self.value,
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


class SafeMap(PaginatedAPIMixin, db.Model):
	#mapping to safe values
	id = db.Column(db.String(128), index=True, unique=True, primary_key=True)
	value = db.Column(db.String(128))
	token_id = db.Column(db.String(128), db.ForeignKey('profile.token_id'))
	field_name = db.Column(db.String(128))
	external_value = db.Column(db.String(2048))
	created = db.Column(db.DateTime(), default=datetime.utcnow)
	updated = db.Column(db.DateTime(), default=datetime.utcnow)

	def __repr__(self):
		return '<MaskMap {}>'.format(self.id)

	def to_dict(self):
		data = {
            'id': self.id,
            'value': self.value,
            'token_id': self.token_id,
            'field_name':self.field_name,
            'external_value': self.external_value,
            'created': self.created.isoformat()+'Z',
            'updated': self.updated.isoformat()+'Z',
        }
		return data

	def from_dict(self, data, new_safe_map=False):
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

	def to_dict(self):
		data = {
            'id': self.id,
            'token_id': self.token_id,
            'message_type': self.message_type,
            'message_format': self.message_format,
            'incoming_endpoint': self.incoming_endpoint,
            'unmasked_data': self.unmasked_data,
            'masked_data': self.masked_data,
            'created': self.created.isoformat()+'Z',
            'updated': self.updated.isoformat()+'Z',
        }
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