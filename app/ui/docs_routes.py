from flask import render_template
from flask_login import current_user, login_required

from app import app
from app.plugins.general_helper import first_time_check


@app.route('/docs', methods=['GET'])
@login_required
def docs_main():
    first_time_check('review_docs', current_user, flash_desc=False)
    return render_template('docs.html', account=current_user.to_dict())
