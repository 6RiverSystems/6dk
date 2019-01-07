import json

from app import db, logger, dk_profile
from app.models import Profile
from datetime import datetime


def create_new_profile(data):
	profile_data = dk_profile.make_profile()
	data['data'] = json.dumps(profile_data)
	logger.debug('creating new profile')
	profile = Profile()
	profile.from_dict(data, new_profile=True)
	db.session.add(profile)
	db.session.commit()
	logger.debug('created new profile for {0}: {1}'.format(data['email'], 
													profile_data['friendly_name']))
	return profile.to_dict()


def make_profile_active(token, current_user):
	profile_list = Profile.query.filter_by(email=current_user.email).all()
	for profile in profile_list:
		data = json.loads(profile.data)
		if profile.token_id == token:
			data['active'] = True
			current_user.active_profile = token
			current_user.updated = datetime.utcnow()
		else:
			data['active'] = False
		profile.updated = datetime.utcnow()
		profile.data = json.dumps(data)
	db.session.commit()
	return Profile.query.filter_by(token_id=token).first().to_dict()


def remove_profile(token):
	profile = Profile.query.filter_by(token_id=token).first()
	profile.deleted = True
	profile.updated = datetime.utcnow()
	db.session.commit()