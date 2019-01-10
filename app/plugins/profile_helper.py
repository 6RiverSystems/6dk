import json

from flask import render_template, jsonify, redirect, url_for
from app import db, logger, dk_profile
from app.ui._forms import NorthboundMessageSettings
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


def serve_northbound_settings_form(token, message_settings):
    form = NorthboundMessageSettings()
    form.wms_host.data = message_settings['wms_host']
    form.wms_port.data = message_settings['wms_port']
    form.wms_path.data = message_settings['wms_path']
    if len(message_settings['wms_headers'])>0:
        form.wms_headers.data = message_settings['wms_headers']
    else:
        form.wms_headers.data = '\n'.join(message_settings['wms_headers'])
    form.send_confirmations = message_settings['send']
    action = "javascript:apply_profile_settings('{0}', '{1}', '{2}');".format(
    												token, 
													'northbound', 
													message_settings['name'])
    return jsonify({
                    'html': render_template('embedded_form.html',
                            form=form,
                            formname='Edit {} settings.'.format(
                            						message_settings['name']),
                            action=action,
                            id='edit-{0}-{1}'.format(token, 
                            						message_settings['name']))
                    }) 


def serve_southbound_settings_form(token, message_settings):
	return


def update_northbound_settings(token, message_settings, new_settings):
	print(new_settings)
	profile_obj = Profile.query.filter_by(token_id=token).first()
	profile = profile_obj.to_dict()
	msg_index = profile['data']['northbound_messages'].index(next(message 
							for message in profile['data']['northbound_messages'] 
							if message['name']==message_settings['name']))
	profile_settings = profile['data']['northbound_messages'][msg_index]
	profile_settings['wms_host'] = new_settings['wms_host'][0]
	profile_settings['wms_port'] = int(new_settings['wms_port'][0])
	profile_settings['wms_path'] = new_settings['wms_path'][0]
	profile_settings['send'] = convert_confirmations(new_settings['send_confirmations'][0])
	profile_settings['wms_headers'] =  new_settings['wms_headers'][0].splitlines()
	profile_obj.data = json.dumps(profile['data'])
	db.session.commit()
	return redirect(url_for('retrieve_settings', token=token))

def convert_confirmations(conf):
	if conf.lower()=='y':
		return True
	else:
		return False

def update_southbound_settings(token, message_settings, new_settings):
	return redirect(url_for('retrieve_settings', token=token))


def display_message_settings(token, message_settings, message_direction):
    return jsonify({
                    'html': render_template('profiles/profile_view_message_settings.html',
                            message_direction=message_direction,
                            message_settings=message_settings)
                    }) 