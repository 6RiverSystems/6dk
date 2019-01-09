from flask import render_template
from flask_login import current_user, login_required

from app import app, rule
from app.models import Profile


@app.route('/feed', methods=['GET'])
@login_required
def feed_main():
    user_profiles = current_user.load_user_profiles()
    token_ids = [
                    profile['token_id'] 
                    for profile in user_profiles
                ]
    messages = Profile.load_messages(token_ids, 
    								parse_timestamps=True)
    valid_northbound = rule.get_northbound_messages()
    return render_template('feed.html', messages=messages, 
    						valid_northbound=valid_northbound)