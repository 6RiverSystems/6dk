from flask import render_template, jsonify
from flask_login import login_required, current_user

from app import app


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('home.html')


@app.route('/check-welcome', methods=['POST'])
@login_required
def check_welcome(jsonified=True):
	persona = current_user.to_dict()['data']
	outstanding = sum([step['open'] for step in persona['startup_steps']])
	if outstanding:
		incomplete = True
	else:
		incomplete = False
	data = {
			'html': render_template('welcome.html',persona=persona),
			'incomplete': incomplete
			}
	if jsonified:
		return jsonify(data)
	else:
		return data