from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from app import app, rule


@app.route('/explorer', methods=['GET'])
@login_required
def explorer_main():
	profile = current_user.get_active_profile()
	if profile:
		messages = rule.get_southbound_messages()
		return render_template('explorer/explorer_main.html', 
								messages=messages,
								profile=profile,
								header='Explorer',
								)
	else:
		flash('You must activate a profile before using Explorer.')
		return redirect(url_for('profiles_main'))