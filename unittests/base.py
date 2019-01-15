import json
import unittest

from app import app, db, dk_profile
from app.models import User, Profile
from app.plugins.general_helper import check_for_keys


class sixDKTests(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()


	def get_payload(self, filename, load_json=False):
		with open('testdata/'+filename, 'r') as f:
			if load_json:
				return json.loads(f.read())
			return f.read()

	def remove_keys(self, data, load_json=False, keys=[]):
		if load_json:
			return {k: v for (k,v) in data.items() if k not in keys}
		else:
			return json.dumps({k: v for (k,v) in json.loads(data).items() 
									if k not in keys})

	def admin_header(self):
		return {'6Dk-Admin-Token': '09dfe030-e97d-4c59-b440-c936d212e0ab'}


	def create_user(self, email=None, first_name=None, last_name=None, 
					password=None, include_profile=False):
		data = self.get_payload('sdk-user.json', load_json=True)
		if email:
			data['email'] = email
		if first_name:
			data['first_name'] = first_name
		if last_name:
			data['last_name'] = last_name
		if password:
			data['password'] = password
		user = User()
		user.from_dict(data, new_user=True)
		user.set_password(data['password'])
		db.session.add(user)
		db.session.commit()
		user = user.to_dict()
		if include_profile:
			data = {'user': user['id']}
			profile_data = dk_profile.make_profile()
			data['data'] = json.dumps(profile_data)
			profile = Profile()
			profile.from_dict(data, new_profile=True)
			db.session.add(profile)
			db.session.commit()
			return user, profile.to_dict()
		else:
			return user
