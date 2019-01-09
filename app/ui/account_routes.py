from flask import render_template
from flask_login import current_user, login_required

from app import app


@app.route('/account', methods=['GET'])
@login_required
def account_main():
    return render_template('account.html', account=current_user.to_dict())