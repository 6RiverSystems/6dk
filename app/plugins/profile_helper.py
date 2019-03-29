import json

from flask import render_template, jsonify, redirect, url_for
from app import db, logger, dk_profile, rule
from app.ui._forms import (NbMessageHttps, NbMessageSftp, ProfileForm)
from app.models import Profile
from datetime import datetime


def create_new_profile(data, as_obj=False):
    profile_data = dk_profile.make_profile()
    data['data'] = json.dumps(profile_data)
    logger.debug('creating new profile')
    profile = Profile()
    profile.from_dict(data, new_profile=True)
    db.session.add(profile)
    db.session.commit()
    logger.debug('created new profile for {0}: {1}'.format(data['user'],
                                                           profile_data['friendly_name']))
    if as_obj:
        return profile
    else:
        return profile.to_dict()


def make_profile_active(token, current_user):
    profile_list = Profile.query.filter_by(user=current_user.id).all()
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
    return profile.to_dict()


def restore_profile(token):
    profile = Profile.query.filter_by(token_id=token).first()
    profile.deleted = False
    profile.updated = datetime.utcnow()
    db.session.commit()
    return profile.to_dict()


def make_profile_copy(token, user, same_name=False):
    profile = Profile.query.filter_by(token_id=token).first().to_dict()
    new_profile = create_new_profile({'user': user}, as_obj=True)
    if same_name:
        new_profile_name = profile['data']['friendly_name']
    else:
        new_profile_name = json.loads(new_profile.data)['friendly_name']
    old_name = profile['data']['friendly_name']
    profile['data']['friendly_name'] = new_profile_name
    profile['data']['active'] = False
    new_profile.data = json.dumps(profile['data'])
    db.session.commit()
    return new_profile.to_dict(), old_name


def serve_edit_profile_form(token):
    profile = Profile.query.filter_by(token_id=token).first().to_dict()
    form = ProfileForm()
    form.name.data = profile['data']['friendly_name']
    action = url_for('edit_profile', token=token)
    return jsonify({
        'html': render_template('embedded_form.html',
                                form=form,
                                formname='Edit {}'.format(token),
                                action=action,
                                id='edit-{0}'.format(token))
    })


def serve_forward_profile_form(token, form):
    profile = Profile.query.filter_by(token_id=token).first().to_dict()
    action = url_for('forward_profile', token=token)
    return jsonify({
        'html': render_template('embedded_form.html',
                                form=form,
                                formname='Forward {}'.format(
                                    profile['data']['friendly_name']),
                                action=action,
                                id='forward-{0}'.format(token))
    })


def serve_northbound_settings_form(token, message_settings):
    if message_settings['transport'] == 'HTTPS':
        form = NbMessageHttps()
        if len(message_settings['wms_headers']) > 0:
            form.wms_headers.data = '\n'.join(message_settings['wms_headers'])
    elif message_settings['transport'] == 'SFTP':
        form = NbMessageSftp()
        form.wms_username.data = message_settings['wms_username']
        form.wms_password.data = message_settings['wms_password']
    form.wms_host.data = message_settings['wms_host']
    form.wms_port.data = message_settings['wms_port']
    form.wms_path.data = message_settings['wms_path']
    form.send_confirmations.data = message_settings['send']
    action = "javascript:apply_profile_settings('{0}', '{1}', '{2}');".format(
        token,
        'northbound',
        message_settings['name'])
    foot_url_link = "javascript:get_message_transport_selector('{0}', '{1}', '{2}');".format(
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
                                                         message_settings['name']),
                                foot_text='Currently viewing settings for {0} via {1} transport.'.format(
                                    message_settings['format'],
                                    message_settings['transport']),
                                foot_url_text='Need something else?',
                                foot_url_link=foot_url_link
                                ),

    })


def serve_transport_selector_form(token, message_settings, direction):
    transports = rule.get_message_transports(message_settings)
    return jsonify({
        'html': render_template('profiles/profile_transport_selector.html',
                                transports=transports,
                                message_settings=message_settings,
                                token=token,
                                direction=direction),
    })


def serve_southbound_settings_form(token, message_settings):
    return


def update_northbound_settings(token, message_settings, new_settings):
    profile_obj = Profile.query.filter_by(token_id=token).first()
    profile = profile_obj.to_dict()
    msg_index = profile['data']['northbound_messages'].index(next(message
                                                                  for message in profile['data']['northbound_messages']
                                                                  if message['name'] == message_settings['name']))
    profile_settings = profile['data']['northbound_messages'][msg_index]
    profile_settings['wms_host'] = new_settings['wms_host'][0]
    profile_settings['wms_port'] = new_settings['wms_port'][0]
    if 'wms_path' in new_settings.keys():
        profile_settings['wms_path'] = new_settings['wms_path'][0]
    if 'send_confirmations' in new_settings.keys():
        profile_settings['send'] = convert_confirmations(
            new_settings['send_confirmations'][0])
    else:
        profile_settings['send'] = False
    if 'wms_headers' in new_settings.keys():
        profile_settings['wms_headers'] = new_settings[
            'wms_headers'][0].splitlines()
    if 'wms_username' in new_settings.keys():
        profile_settings['wms_username'] = new_settings['wms_username'][0]
    if 'wms_password' in new_settings.keys():
        profile_settings['wms_password'] = new_settings['wms_password'][0]
    profile_obj.data = json.dumps(profile['data'])
    db.session.commit()


def convert_confirmations(conf):
    if conf.lower() == 'y':
        return True
    else:
        return False


def display_message_settings(token, message_settings, message_direction):
    return jsonify({
        'html': render_template('profiles/profile_view_message_settings.html',
                                message_direction=message_direction,
                                message_settings=message_settings)
    })
