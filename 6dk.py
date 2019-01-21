from app import app, db, rule
from app.models import User, Profile, MaskMap, Message, MessageTransmission

@app.shell_context_processor
def make_shell_context():
    return {
    		'db': db, 
    		'app': app,
    		'rule': rule,
    		'User': User, 
    		'Profile': Profile,
    		'MaskMap': MaskMap,
    		'Message': Message,
    		'MessageTransmission': MessageTransmission
    		}