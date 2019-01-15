from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, 
					IntegerField, TextAreaField, SelectMultipleField)
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset')


class EditAccount(FlaskForm):
	first_name = StringField('Email', validators=[DataRequired()])
	last_name = StringField('Email', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Save')


class ChangePassword(FlaskForm):
    password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(),
    													EqualTo('new_password')])
    submit = SubmitField('Save')


class ProfileForm(FlaskForm):
	name = StringField('Profile Name', validators=[DataRequired()])
	submit = SubmitField('Submit')


class ForwardProfileForm(FlaskForm):
	recipient = StringField('Recipient Email', validators=[DataRequired()])
	submit = SubmitField('Submit')


class FeedForm(FlaskForm):
	message_type = SelectMultipleField('Message Type')
	profile = SelectMultipleField('Profile')
	sent_after = StringField('Sent After')
	sent_before = StringField('Sent Before')
	q = StringField('Search Term', validators=[Length(min=3)])
	submit = SubmitField('Search')


class ExplorerMessage(FlaskForm):
	wms_headers = TextAreaField('Payload', validators=[DataRequired()])
	submit = SubmitField('Post')


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
	submit = SubmitField('Submit')