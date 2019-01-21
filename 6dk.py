from app import app, db, rule, dk_profile, dk_user
from app.models import User, Profile, MaskMap, Message, MessageTransmission

@app.shell_context_processor
def make_shell_context():
    return {
    		'db': db, 
    		'app': app,
    		'rule': rule,
            'dk_profile': dk_profile,
            'dk_user': dk_user,
    		'User': User, 
    		'Profile': Profile,
    		'MaskMap': MaskMap,
    		'Message': Message,
    		'MessageTransmission': MessageTransmission
    		}