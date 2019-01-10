from app import app, db
from app.models import User, Profile, MaskMap, Message, MessageTransmission

@app.shell_context_processor
def make_shell_context():
    return {
    		'db': db, 
    		'User': User, 
    		'Profile': Profile,
    		'MaskMap': MaskMap,
    		'Message': Message,
    		'MessageTransmission': MessageTransmission}