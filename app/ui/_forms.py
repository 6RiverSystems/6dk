from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, 
					IntegerField, TextAreaField)
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class NorthboundMessageSettings(FlaskForm):
	wms_host = StringField('WMS Host', validators=[DataRequired()],
						render_kw={"placeholder": "https://wms.warehouse.com"})
	wms_port = IntegerField('WMS Port', validators=[DataRequired()],
						render_kw={"placeholder": "443"})
	wms_path = StringField('WMS Path', validators=[DataRequired()],
						render_kw={"placeholder": "northbound/messages"})
	wms_headers = TextAreaField('WMS Headers', validators=[DataRequired()],
						render_kw={"placeholder": "Content-Type: application/json\nAccept: application/json"})
	send_confirmations = BooleanField('Send Confirmations')
	submit = SubmitField('Save')