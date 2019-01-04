from flask import render_template
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db

@login_required
@app.route('/', methods=['GET'])
def home():
	return render_template('base.html')

@app.route('/login', methods=['GET'])
def login():
	return render_template('login.html')


@app.route('/docs', methods=['GET'])
def docs():
	return render_template('docs.html')

"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

"""

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
