import json
from datetime import datetime

from flask import render_template, url_for, request, flash, jsonify, redirect
from flask_login import current_user, login_required

from app import app, db, rule
from app.models import User
from app.ui._forms import EditAccount, ChangePassword, ChooseMessages
from app.plugins.mail_helper import send_password_reset_done_email
from app.plugins.general_helper import (first_time_check, reset_onboarding, 
										is_step_completed)
from app.ui.application_routes import check_welcome


@app.route('/account', methods=['GET'])
@login_required
def account_main():
	if is_step_completed('set_pwd', current_user):
		first_time_check('choose_messages', current_user, edit_entry=False)
	else:
		first_time_check('set_pwd', current_user, edit_entry=False)
	onboarding = check_welcome(jsonified=False)
	return render_template('account.html', account=current_user.to_dict(), 
							onboarding=onboarding)


@app.route('/account/<user_id>/reset-onboarding', methods=['GET'])
@login_required
def account_onboarding_reset(user_id):
	if current_user.id==user_id and not check_welcome(jsonified=False)['incomplete']:
		reset_onboarding(current_user)
	return redirect(url_for('index'))


@app.route('/account/edit', methods=['GET','POST'])
@login_required
def account_edit():
	form = EditAccount()
	if form.validate_on_submit():
		existing = User.query.filter_by(email=form.email.data).first()
		if not current_user.check_password(form.password.data):
			flash('Incorrect password.')
		elif existing and existing != current_user:
			flash('Email address in use by another user.')
		else:
			current_user.first_name = form.first_name.data
			current_user.last_name = form.last_name.data
			current_user.email = form.email.data
			current_user.updated = datetime.utcnow()
			db.session.commit()
			flash('Successfully updated account')
	elif request.method == 'GET':
		form.first_name.data = current_user.first_name
		form.last_name.data = current_user.last_name
		form.email.data = current_user.email
		return jsonify({
					'html': render_template('embedded_form.html',
							form=form,
							formname='Edit Account',
							action=url_for('account_edit'),
							id='edit-account-form')
					})
	return redirect(url_for('account_main'))



@app.route('/account/change-password', methods=['GET', 'POST'])
@login_required
def account_change_password():
	form = ChangePassword()
	if form.validate_on_submit():
		if not current_user.check_password(form.password.data):
			flash('Incorrect password.')
		elif current_user.check_password(form.password.data) \
				and current_user.check_password(form.new_password.data):
			flash('New and old passwords are the same.')
		elif len(form.new_password.data) < 8:
			flash('Password must be at least 8 characters long')
		else:
			current_user.set_password(form.new_password.data)
			db.session.commit()
			flash('Successfully changed password')
			first_time_check('set_pwd', current_user, flash_desc=False)
			send_password_reset_done_email(current_user)
	elif request.method == 'GET':
		return jsonify({
					'html': render_template('embedded_form.html',
							form=form,
							formname='Change Password',
							action=url_for('account_change_password'),
							id='change-password-form')
					})
	return redirect(url_for('account_main'))


@app.route('/account/choose-messages', methods=['GET', 'POST'])
@login_required
def account_choose_messages():
	form = ChooseMessages()
	form.southbound_messages.choices = [(msg, msg) 
										for msg in rule.get_messages_list('southbound')]
	form.northbound_messages.choices = [(msg, msg) 
										for msg in rule.get_messages_list('northbound')]
	if form.validate_on_submit():
		data = current_user.to_dict()['data']
		data['message_types']['northbound'] = form.northbound_messages.data
		data['message_types']['southbound'] = form.southbound_messages.data
		current_user.data = json.dumps(data)
		db.session.commit()
		first_time_check('choose_messages', current_user, flash_desc=False)
	elif request.method == 'GET':
		data = current_user.to_dict()['data']['message_types']
		form.southbound_messages.data = data['southbound']
		form.northbound_messages.data = data['northbound']
		return jsonify({
					'html': render_template('embedded_form.html',
							form=form,
							formname='Choose Messages',
							action=url_for('account_choose_messages'),
							id='choose-messages-form')
					})
	return redirect(url_for('account_main'))