import json

from flask import render_template, redirect, url_for, flash, jsonify, request
from flask_login import current_user, login_required
from urllib.parse import parse_qs

from app import app, db, rule
from app.ui._forms import ForwardProfileForm
from app.models import Profile, User
from app.plugins.profile_helper import (create_new_profile, make_profile_active,
                                        remove_profile, restore_profile,
                                        make_profile_copy,
                                        serve_edit_profile_form,
                                        serve_northbound_settings_form, 
                                        serve_southbound_settings_form,
                                        serve_forward_profile_form,
                                        update_northbound_settings,
                                        display_message_settings,
                                        serve_transport_selector_form)
from app.plugins.mail_helper import (send_forward_profile_email, 
                                        send_accept_profile_email)
from app.plugins.general_helper import first_time_check, is_step_completed


@app.route('/profiles', methods=['GET'])
@login_required
def profiles_main():
    if is_step_completed('create_profile', current_user):
        first_time_check('mod_profile', current_user, edit_entry=False)
    else:
        first_time_check('create_profile', current_user, edit_entry=False)
    user_profiles = current_user.load_user_profiles()
    deleted_profiles = current_user.load_user_profiles(deleted=True)
    limit = app.config['MAX_PROFILE_COUNT']
    return render_template('profiles/profiles_main.html', 
                            user_profiles=user_profiles,
                            deleted_profiles=deleted_profiles,
                            header='Profiles',
                            limit=limit)


@app.route('/profiles/add', methods=['GET', 'POST'])
@login_required
def add_profile():
    user_profiles = current_user.load_user_profiles()
    if len(user_profiles) < app.config['MAX_PROFILE_COUNT']:
        profile = create_new_profile({'user': current_user.id})
        flash('Created new profile: {}'.format(profile['data']['friendly_name']))
        first_time_check('create_profile', current_user, flash_desc=False)
    else:
        flash('Maximum number of profiles reached')
    return redirect(url_for('profiles_main'))


@app.route('/profiles/<token>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(token):
    if request.method=='GET':
        if not current_user.owns_token(token):
            flash('You do not own token: {}'.format(token)) 
            return redirect(url_for('profiles_main'))      
        else:
            return serve_edit_profile_form(token)
    else:
        profile = Profile.query.filter_by(token_id=token).first()
        profile_data = json.loads(profile.data)
        old_name = profile_data['friendly_name']
        profile_data['friendly_name'] = request.form['name']
        profile.data = json.dumps(profile_data)
        db.session.commit()
        flash('Renamed profile: {0} >> {1}'.format(old_name, 
                                                        request.form['name']))
        return redirect(url_for('profiles_main'))
    

@app.route('/profiles/<token>/forward', methods=['GET', 'POST'])
@login_required
def forward_profile(token):
    form = ForwardProfileForm()
    if request.method=='GET':
        if not current_user.owns_token(token):
            flash('You do not own token: {}'.format(token)) 
            return redirect(url_for('profiles_main'))      
        else:
            return serve_forward_profile_form(token, form)
    else:
        recipient = User.query.filter_by(email=form.recipient.data).first()
        if not recipient:
            flash('Recipient not found: {}'.format(form.recipient.data))
        elif recipient.id == current_user.id:
            flash('You cannot forward a profile to yourself.')
        else:
            send_forward_profile_email(current_user, recipient, token)
            flash('Forwarded copy of profile to: {}'.format(form.recipient.data))
        return redirect(url_for('profiles_main'))


@app.route('/profiles/<token>/receive', methods=['GET'])
@login_required
def receive_profile(token):
    token_data = current_user.receive_forward_profile_token(token)
    if token_data:
        user_profiles = current_user.load_user_profiles()
        if len(user_profiles) < app.config['MAX_PROFILE_COUNT']:
            profile, old_name = make_profile_copy(token_data['profile'], 
                                                current_user.id, 
                                                same_name=True)
            flash('Successfully received profile: {}'.format(
                                                    profile['data']['friendly_name']))

            send_accept_profile_email(token_data['source'], current_user, 
                                                    token_data['profile'])
        else:
            flash('Maximum number of profiles reached. Remove a profile and try again.')
    else:
        flash('Invalid forward profile token')
    return redirect(url_for('profiles_main'))


@app.route('/profiles/<token>/copy', methods=['GET', 'POST'])
@login_required
def copy_profile(token):
    user_profiles = current_user.load_user_profiles()
    if len(user_profiles) < app.config['MAX_PROFILE_COUNT']:
        if not current_user.owns_token(token):
            flash('You do not own token: {}'.format(token))       
        else:
            profile, old_name = make_profile_copy(token, current_user.id)
            flash('Copied profile: {0} >> {1}'.format(old_name, 
                                            profile['data']['friendly_name']))
    else:
        flash('Maximum number of profiles reached')
    return redirect(url_for('profiles_main'))


@app.route('/profiles/<token>/delete', methods=['GET', 'POST'])
@login_required
def delete_profile(token):
    profile = Profile.query.filter_by(token_id=token).first().to_dict()
    if token == current_user.active_profile:
        flash('Cannot delete active profile: {}'.format(profile['data']['friendly_name']))
    elif not current_user.owns_token(token):
        flash('You do not own token: {}'.format(token))       
    else:
        profile = remove_profile(token)
        flash('Deleted profile: {}'.format(profile['data']['friendly_name']))
    return redirect(url_for('profiles_main'))


@app.route('/profiles/<token>/restore', methods=['GET', 'POST'])
@login_required
def undelete_profile(token):
    if not current_user.owns_token(token):
        flash('You do not own token: {}'.format(token))       
    else:
        user_profiles = current_user.load_user_profiles()
        if len(user_profiles) < app.config['MAX_PROFILE_COUNT']:
            profile = restore_profile(token)
            flash('Restored profile: {}'.format(profile['data']['friendly_name']))
        else:
            flash('Maximum number of profiles reached')
    return redirect(url_for('profiles_main'))


@app.route('/profiles/<token>/activate', methods=['GET', 'POST'])
@login_required
def activate_profile(token):
    if not current_user.owns_token(token):
        flash('You do not own token: {}'.format(token))
    else:      
        profile = make_profile_active(token, current_user)
        flash('Profile activated: {}'.format(profile['data']['friendly_name']))
    return redirect(url_for('profiles_main'))


@app.route('/profiles/<token>/settings', methods=['GET', 'POST'])
@login_required
def retrieve_settings(token):
    if not current_user.owns_token(token):
        return jsonify({'html':'You do not own token: {}'.format(token)})
    else:
        profile = Profile.query.filter_by(token_id=token).first().to_dict()
        user = current_user.to_dict()
        has_northbound = not set(user['data']['message_types']['northbound']
                            ).isdisjoint([msg['name'] for msg in profile['data']['northbound_messages']])
        has_southbound = not set(user['data']['message_types']['southbound']
                            ).isdisjoint([msg['name'] for msg in profile['data']['southbound_messages']])
        return jsonify({
                        'html': render_template('profiles/profile_settings.html',
                                                profile=profile,
                                                user=user,
                                                has_northbound=has_northbound,
                                                has_southbound=has_southbound),
                        'data': profile['data']
                        })


@app.route('/profiles/<token>/<message_direction>/<message_type>/settings/<action>', 
            methods=['GET', 'POST'])
@login_required
def message_settings(token, message_direction, message_type, action):
    if not current_user.owns_token(token):
        return jsonify({'html':'You do not own token: {}'.format(token)})
    else:
        profile = Profile.query.filter_by(token_id=token).first().to_dict()
        if message_direction == 'northbound':
            message_settings = next(message 
                                    for message in profile['data']['northbound_messages']
                                    if message['name']==message_type)
            if action=='retrieve':
                return serve_northbound_settings_form(token, message_settings)
            elif action=='apply':
                new_settings = parse_qs(request.form.to_dict()['formdata'])
                first_time_check('mod_profile', current_user, flash_desc=False)
                update_northbound_settings(token, message_settings, 
                                                new_settings)
                return retrieve_settings(token)
            elif action=='view':
                return display_message_settings(token, message_settings, 
                                                'northbound') 
            elif action=='change-transport':
                return serve_transport_selector_form(token, message_settings, 'northbound')            
        elif message_direction == 'southbound':
            message_settings = next(message 
                                    for message in profile['data']['southbound_messages']
                                    if message['name']==message_type)
            if action=='retrieve':
                return serve_southbound_settings_form(token, message_settings)
            elif action=='change-transport':
                return serve_transport_selector_form(token, message_settings, 'southbound')   


@app.route('/profiles/<token>/<message_direction>/<message_type>/settings/apply-transport/<message_format>/<message_transport>', 
            methods=['POST'])
@login_required
def change_message_transport(token, message_direction, message_type, message_format, message_transport):
    if not current_user.owns_token(token):
        return jsonify({'html':'You do not own token: {}'.format(token)})
    else:
        first_time_check('mod_profile', current_user, flash_desc=False)
        profile_obj = Profile.query.filter_by(token_id=token).first()
        profile = profile_obj.to_dict()
        message_settings = next(message for message in profile['data'][message_direction+'_messages'] 
                                if message['name']==message_type)
        transports = rule.get_message_transports(message_settings)
        valid = next((transport for transport in transports 
                        if transport['format']==message_format 
                        and transport['transport']==message_transport), None)
        if valid:
            message_settings['format'] = message_format
            message_settings['transport'] = message_transport
            message_settings['send'] = False
            profile_obj.data = json.dumps(profile['data'])
            db.session.commit()
            if message_direction=='northbound':
                return message_settings(token, message_direction, message_type, 'retrieve')
            else:
                return retrieve_settings(token)
        else:
            return jsonify({'html':'Invalid message transport'})  