import json

from flask import render_template, redirect, url_for, flash, jsonify, request
from flask_login import current_user, login_required
from urllib.parse import parse_qs

from app import app, db
from app.models import Profile
from app.plugins.profile_helper import (create_new_profile, make_profile_active,
                                        remove_profile, restore_profile,
                                        make_profile_copy,
                                        serve_edit_profile_form,
                                        serve_northbound_settings_form, 
                                        serve_southbound_settings_form,
                                        update_northbound_settings,
                                        update_southbound_settings,
                                        display_message_settings)


@app.route('/profiles', methods=['GET'])
@login_required
def profiles_main():
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
        flash('Renamed profile: {0} >> {1}'.format(old_name, request.form['name']))
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
            flash('Copied profile: {0} >> {1}'.format(old_name, profile['data']['friendly_name']))
    else:
        flash('Maximum number of profiles reached')
    return redirect(url_for('profiles_main'))


@app.route('/profiles/<token>/delete', methods=['GET', 'POST'])
@login_required
def delete_profile(token):
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
def activate_profile(token):
    if not current_user.owns_token(token):
        flash('You do not own token: {}'.format(token))
    else:      
        profile = make_profile_active(token, current_user)
        flash('Profile activated: {}'.format(profile['data']['friendly_name']))
    return redirect(url_for('profiles_main'))


@app.route('/profiles/<token>/settings', methods=['GET', 'POST'])
def retrieve_settings(token):
    if not current_user.owns_token(token):
        return jsonify({'html':'You do not own token: {}'.format(token)})
    else:
        profile = Profile.query.filter_by(token_id=token).first().to_dict()
        return jsonify({
                        'html': render_template('profiles/profile_settings.html',
                                                profile=profile),
                        'data': profile['data']
                        })


@app.route('/profiles/<token>/<message_direction>/<message_type>/settings/<action>', 
            methods=['GET', 'POST'])
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
                return update_northbound_settings(token, message_settings, 
                                                new_settings)
            elif action=='view':
                return display_message_settings(token, message_settings, 
                                                'northbound')                
        elif message_direction == 'southbound':
            message_settings = next(message 
                                    for message in profile['data']['southbound_messages']
                                    if message['name']==message_type)
            if action=='retrieve':
                return serve_southbound_settings_form(token, message_settings)
            elif action=='apply':
                new_settings = parse_qs(request.form.to_dict()['formdata'])
                return display_message_settings(token, message_settings, 
                                                'southbound')  
            elif action=='view':
                return display_southbound_settings(token, message_settings)    