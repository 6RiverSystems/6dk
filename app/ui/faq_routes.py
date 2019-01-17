import json

from flask import render_template
from flask_login import login_required

from app import app

@app.route('/faq', methods=['GET'])
@login_required
def faq_main():
	with open('app/templates/json/faqs.json', 'r') as f:
		faqs = json.loads(f.read())
	return render_template('faq.html', faqs=faqs)