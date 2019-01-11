import json
import sys
from datetime import datetime

from flask import render_template, jsonify
from flask_login import current_user, login_required

from app import app, db, rule
from app.models import Profile, Message


@app.route('/feed', methods=['GET'])
@login_required
def feed_main():
    user_profiles = current_user.load_user_profiles()
    current_user.last_feed_load_time = datetime.utcnow()
    db.session.commit()
    token_ids = [
                    profile['token_id'] 
                    for profile in user_profiles
                ]
    messages = Profile.load_messages(token_ids, 
    								parse_timestamps=True)
    valid_northbound = rule.get_northbound_messages()
    message_types = rule.get_all_messages()
    message_types = message_types + [msg+'-response' for msg in message_types]
    return render_template('feed/feed.html', messages=messages, 
    						valid_northbound=valid_northbound,
                            user_profiles=user_profiles,
                            message_types=message_types)


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


@app.route('/feed/new-messages', methods=['GET', 'POST'])
@login_required
def new_messages():
    return jsonify({'count': current_user.new_messages()})
