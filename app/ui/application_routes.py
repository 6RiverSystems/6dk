from flask import render_template, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user

from app import app
from app.plugins.general_helper import user_accept_onboarding


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('home.html')


@app.route('/check-welcome', methods=['POST'])
@login_required
def check_welcome(jsonified=True):
    persona = current_user.to_dict()['data']
    if persona['accepted_onboarding']:
        incomplete = False
    else:
        incomplete = True
    outstanding = sum([step['open'] for step in persona['startup_steps']])
    data = {
        'html': render_template('welcome.html', persona=persona,
                                outstanding=outstanding),
        'incomplete': incomplete,
        'outstanding': outstanding
    }
    if jsonified:
        return jsonify(data)
    else:
        return data


@app.route('/<user_id>/accept-onboarding', methods=['GET'])
@login_required
def accept_onboarding(user_id):
    if current_user.id == user_id and not check_welcome(jsonified=False)['outstanding']:
        user_accept_onboarding(current_user)
        flash("You're all set!")
    return redirect(url_for('index'))
