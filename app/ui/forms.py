from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired
from app.models import Persistence


class FormatterPayloadForm(FlaskForm):
	#form for submitting messages to be formatted
	type_choices = [
				('json','JSON payload of available fields'),
				('xml','XML payload of available fields'),
				('comma-csv','comma-separated variables'),
				('caret-csv','caret-separated variables'),
				('fields','list of available fields'),
				]
	msg_choices = [
				('pickWave', 'pickWave')
				]
	data = TextAreaField('Data', validators=[DataRequired()])
	data_type = SelectField('Data Type', choices=type_choices)
	msg_type = SelectField('Message Type', choices=msg_choices)
	submit = SubmitField('Continue')

class FormatterPickWave(FlaskForm):
	groupType = SelectField('Group Type')
	groupID = SelectField('Group ID')
	pickID = SelectField('Pick ID')

	containerID = SelectField('Container ID')
	containerType = SelectField('Container Type')

	sourceLocation = SelectField('Source Location')
	destinationLocation = SelectField('Destination Location')
	eachQuantity = SelectField('Each Quantity')

	UOMQ = SelectField('Unit of Measure Quantity')
	UOM = SelectField('Unit of Measure')
	identifiers = SelectMultipleField('Identifiers')
	name = SelectField('Name')
	description = SelectField('Description')
	imageURL = SelectField('Image URL')
	length = SelectField('Length')
	width = SelectField('Width')
	height = SelectField('Height')
	weight = SelectField('Weight')
	dUOM = SelectField('Dimension Unit Of Measure')
	wUOM = SelectField('Weight Unit of Measure')
	lotID = SelectField('Lot ID')

	expectedShippingDate = SelectField('Expected Shipping Date')
	data = SelectField('Data')