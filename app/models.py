import json
from datetime import datetime
from uuid import uuid4

from flask import url_for
from app import db


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


class Profile(PaginatedAPIMixin, db.Model):
	token_id = db.Column(db.String(128), index=True, unique=True, primary_key=True)
	email  = db.Column(db.String(128))
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


class MaskPath(PaginatedAPIMixin, db.Model):
	id = db.Column(db.String(128), index=True, unique=True, primary_key=True)
	message_type = db.Column(db.String(128))
	key_path = db.Column(db.String(2048), unique=True)
	field_name = db.Column(db.String(128))
	message_format = db.Column(db.String(128))
	created = db.Column(db.DateTime(), default=datetime.utcnow)
	updated = db.Column(db.DateTime(), default=datetime.utcnow)

	def __repr__(self):
		return '<MaskPath {}>'.format(self.key_path)

	def to_dict(self):
		data = {
            'id': self.id,
            'message_type': self.message_type,
            'key_path': self.key_path,
            'field_name': self.field_name,
            'message_format': self.message_format,
            'created': self.created.isoformat()+'Z',
            'updated': self.updated.isoformat()+'Z',
        }
		return data

	def from_dict(self, data, new_mask_path=False):
		for field in ['message_type', 'key_path', 'field_name', 'message_format']:
			if field in data:
				setattr(self, field, data[field])
		if new_mask_path:
				setattr(self, 'id', str(uuid4()))
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
		return '<MaskList {}>'.format(self.id)

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