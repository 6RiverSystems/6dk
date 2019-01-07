from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db, rule
from app.models import User, Profile
from app.ui.forms import LoginForm
from app.plugins.profile_helper import (create_new_profile, make_profile_active,
                                        remove_profile)

#-----------------------------------ERRORS-------------------------------------#


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500


#---------------------------------AUTHENTICATION-------------------------------#


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, deleted=False).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


#---------------------------------APPLICATION----------------------------------#


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('home.html')



#----------------------------------PROFILES------------------------------------#


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

#----------------------------------EXPLORER------------------------------------#


@app.route('/explorer', methods=['GET'])
@login_required
def explorer_main():
    profile = current_user.get_active_profile()
    messages = rule.get_southbound_messages()
    return render_template('explorer/explorer_main.html', 
                            messages=messages,
                            profile=profile,
                            header='Explorer',
                            )


@app.route('/docs', methods=['GET'])
@login_required
def docs():
	return render_template('docs.html')

