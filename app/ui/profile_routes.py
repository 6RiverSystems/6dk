from flask import render_template, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required

from app import app
from app.models import Profile
from app.plugins.profile_helper import (create_new_profile, make_profile_active,
                                        remove_profile)


@app.route('/profiles', methods=['GET'])
@login_required
def profiles_main():
    user_profiles = current_user.load_user_profiles()
    limit = app.config['MAX_PROFILE_COUNT']
    return render_template('profiles/profiles_main.html', 
                            user_profiles=user_profiles,
                            header='Profiles',
                            limit=limit)


@app.route('/profiles/add', methods=['GET', 'POST'])
@login_required
def add_profile():
    user_profiles = current_user.load_user_profiles()
    if len(user_profiles) < app.config['MAX_PROFILE_COUNT']:
        profile = create_new_profile({'email': current_user.email})
        flash('Created new profile: {}'.format(profile['data']['friendly_name']))
    else:
        flash('Maximum number of profiles created')
    return redirect(url_for('profiles_main'))


@app.route('/profiles/<token>/delete', methods=['GET', 'POST'])
@login_required
def delete_profile(token):
    profile = current_user.get_active_profile()
    if token == current_user.active_profile:
        flash('Cannot delete active profile: {}'.format(profile['data']['friendly_name']))
    elif not current_user.owns_token(token):
        flash('You do not own token: {}'.format(token))       
    else:
        flash('Deleted profile: {}'.format(profile['data']['friendly_name']))
        remove_profile(token)
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
