from flask import render_template
from flask_login import current_user, login_required

from app import app


@app.route('/docs', methods=['GET'])
@login_required
def docs_main():
    return render_template('docs.html', account=current_user.to_dict())