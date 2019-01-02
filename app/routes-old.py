from uuid import uuid4
import json
from flask import render_template, redirect, flash, url_for, jsonify

from app import app, logger, db
from app.models import Persistence
from app.helper import make_config, field_extractor
from app.forms import FormatterPayloadForm

def load_config(token):
	config = Persistence.query.filter_by(tokenId=token).first()
	return config

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
	#home page
	with open('app/templates/content/intro.txt', 'r') as f:
		introtxt = f.read()
	with open('app/templates/content/credentials.txt', 'r') as f:
		credtxt = f.read()
	with open('app/templates/content/data_reqs.txt', 'r') as f:
		reqtxt = f.read()
	with open('app/templates/content/features.json', 'r') as f:
		features = json.loads(f.read())
	with open('app/templates/content/spec.json', 'r') as f:
		spec = json.loads(f.read())
	return render_template('home.html', introtxt=introtxt, credtxt=credtxt, reqtxt=reqtxt,
		features=features, spec=spec)


@app.route('/formatter/<token>', methods=['GET', 'POST'])
def formatter_main(token):
	#message formatter main
	logger.info('{} accessing message formatter'.format(token))
	form = FormatterPayloadForm()
	config = load_config(token)
	if config != None:
		if form.validate_on_submit():
			data = form.data.data
			data_type = form.data_type.data
			msg_type = form.msg_type.data
			errors, fields = field_extractor(token, data, data_type)
			print(errors, fields)
			return redirect(url_for('index'))
		return render_template('form.html', title='Message Formatter', 
								form=form, formname='Message Formatter')
	else:
		flash('Token "{}" is invalid'.format(token))
		return redirect(url_for('index'))


@app.route('/explorer/<token>', methods=['GET', 'POST'])
def explorer(id):
	#message formatter page
	return


#----------------------------API ROUTES-----------------------------------#
@app.route('/api/config/v1/generate', methods=['POST'])
def gen_config():
	token = str(uuid4())
	while load_config(token) != None:
		token =str(uuid4())
	config = make_config(token)
	entry = Persistence(tokenId=token, data=json.dumps(config))
	db.session.add(entry)
	db.session.commit()
	return jsonify({'msg':'OK', 'token':token})
