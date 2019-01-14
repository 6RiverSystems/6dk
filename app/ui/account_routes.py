from datetime import datetime

from flask import render_template, url_for, request, flash, jsonify, redirect
from flask_login import current_user, login_required

from app import app, db
from app.models import User
from app.ui._forms import EditAccount, ChangePassword
from app.plugins.mail_helper import send_password_reset_done_email


@app.route('/account', methods=['GET'])
@login_required
def account_main():
    return render_template('account.html', account=current_user.to_dict())


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