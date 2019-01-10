import json
import sys

from flask import render_template, jsonify
from flask_login import current_user, login_required

from app import app, rule
from app.models import Profile, Message


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
    return render_template('feed/feed.html', messages=messages, 
    						valid_northbound=valid_northbound)


@app.route('/feed/message/<message_id>/<task>', methods=['POST'])
@login_required
def feed_message(message_id, task):
    message = Message.query.filter_by(id=message_id).first(
                                    ).to_dict(parse_timestamps=True,
                                                include_profile=True)
    message_data = json.dumps(json.loads(message['unmasked_data']), indent=4, 
                                                                sort_keys=True)
    size = sys.getsizeof(json.dumps(json.loads(message['unmasked_data'])))
    replays = Message.get_replays(message_id)
    return jsonify({
                    'html': render_template('feed/feed_message.html',
                    message=message,
                    message_data=message_data,
                    size=size,
                    task=task,
                    replays=replays),
                    'data': message
                    })