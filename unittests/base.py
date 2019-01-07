import unittest

from app import app, db


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

