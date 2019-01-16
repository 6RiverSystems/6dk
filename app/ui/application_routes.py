from flask import render_template
from flask_login import login_required

from app import app


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('home.html')
    