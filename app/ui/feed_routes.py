import json
import sys
from datetime import datetime

from flask import render_template, jsonify, url_for, request
from flask_login import current_user, login_required

from app import app, db, rule
from app.ui._forms import FeedForm
from app.models import Profile, Message
from app.plugins.feed_helper import filter_feed

@app.route('/feed', methods=['GET', 'POST'])
@login_required
def feed_main():
    user_profiles = current_user.load_user_profiles()
    current_user.last_feed_load_time = datetime.utcnow()
    db.session.commit()
    filters = {
                'message_type': request.form.getlist('message_type'),
                'profile': request.form.getlist('profile'),
                'sent_after': request.form.get('sent_after'),
                'sent_before': request.form.get('sent_before'),
                'q': request.form.get('q'),
                'page': request.form.get('page', 1, type=int)
                }
    messages, filters = filter_feed(filters, user_profiles)
    valid_northbound = rule.get_northbound_messages()
    form = FeedForm()
    form.message_type.choices = [(msg, msg) for msg in rule.get_all_messages()]
    form.profile.choices = [(profile['token_id'], profile['data']['friendly_name'])
                            for profile in user_profiles]
    form_render = render_template('embedded_form.html',
                        form=form,
                        action=url_for('feed_main'),
                        id='feed-search-form')
    message_block = render_template('feed/feed_messages.html',
                                    valid_northbound=valid_northbound,
                                    messages=messages)
    if filters['page'] == 1:
        return render_template('feed/feed.html', 
                                message_block=message_block, 
        						valid_northbound=valid_northbound,
                                form_render=form_render,
                                filters=filters)
    else:
        return jsonify({'html': message_block})


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
                    'html': render_template('feed/feed_message_options.html',
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
