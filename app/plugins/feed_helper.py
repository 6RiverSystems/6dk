import dateparser
import json
import sys

from flask import render_template, jsonify
import lxml.etree as etree

from app import app
from app.models import Message, Profile


def get_filters(request, email=False):
    filters = {
        'message_type': request.form.getlist('message_type'),
        'profile': request.form.getlist('profile'),
        'sent_after': request.form.get('sent_after'),
        'sent_before': request.form.get('sent_before'),
        'q': request.form.get('q'),
        'page': request.form.get('page', 1, type=int)
    }
    if email:
        filters['email'] = request.form.getlist('email')
    for q in ['q', 'sent_before', 'sent_after']:
        if type(filters[q]) == str:
            if filters[q].lower() in ['none', 'null']:
                filters[q] = None
    if len(filters['message_type']) == 0:
        filters['message_type'] = request.form.getlist('message_type[]')
    if len(filters['profile']) == 0:
        filters['profile'] = request.form.getlist('profile[]')
    return filters


def get_message_data(message_id, task):
    message = Message.query.filter_by(id=message_id).first(
    ).to_dict(parse_timestamps=True,
              include_profile=True)
    err = False
    if message['message_format'] == 'JSON':
        try:
            message_data = json.dumps(
                json.loads(message['unmasked_data']), indent=4,
                sort_keys=True)
        except:
            err = True
    elif message['message_format'] == 'XML':
        try:
            xml = etree.fromstring(message['unmasked_data'].encode('utf-8'))
            message_data = etree.tostring(
                xml, pretty_print=True).decode('utf-8')
        except:
            err = True
    else:
        err = True
    if err:
        message_data = message['unmasked_data']
    size = sys.getsizeof(message['unmasked_data'])
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


def filter_feed(filters, user_profiles, user, return_data=False, order="desc"):
    messages = Message.query
    filtered = False
    valid_types = user['data']['message_types'][
        'northbound'] + user['data']['message_types']['southbound']
    valid_types = valid_types + [msg + '-response' for msg in valid_types]

    if len(filters['message_type']) > 0:
        messages = messages.filter(
            Message.message_type.in_(filters['message_type']))
        filtered = True
    else:
        messages = messages.filter(
            Message.message_type.in_(valid_types))

    if len(filters['profile']) > 0:
        messages = messages.filter(Message.token_id.in_(filters['profile']))
        profiles = Profile.query.filter(
            Profile.token_id.in_(filters['profile'])
        ).all()
        filters['profile_names'] = [p.to_dict()['data']['friendly_name']
                                    for p in profiles]
        filtered = True
    else:
        token_ids = [
            profile['token_id']
            for profile in user_profiles
        ]
        messages = messages.filter(Message.token_id.in_(token_ids))
        filters['profile_names'] = ['all profiles']
    try:
        if filters['sent_after']:
            start = dateparser.parse(filters['sent_after'])
            messages = messages.filter(Message.updated >= start)
            filtered = True
    except:
        pass

    try:
        if filters['sent_before']:
            end = dateparser.parse(filters['sent_before'])
            messages = messages.filter(Message.updated <= end)
            filtered = True
    except:
        pass
    if filters['q']:
        if len(filters['q']) >= 3:
            messages = messages.filter(
                Message.unmasked_data.like(
                    '%{}%'.format(filters['q'])))
            filtered = True
    filters['count'] = messages.count()
    if order == 'desc':
        messages = messages.order_by(
            Message.updated.desc()
        )
    elif order == 'asc':
        messages = messages.order_by(
            Message.updated.asc()
        )
    data = [m.to_dict(include_profile=True, parse_timestamps=True,
                      include_transmissions=True)
            for m in messages.all()]
    filters['transmissions'] = sum(
        [m['transmissions_info']['count'] for m in data])
    if return_data:
        return data, filters
    messages = messages.paginate(
        filters['page'],
        app.config['ELEMENTS_PER_PAGE'],
        False)
    filters['has_next'] = messages.has_next
    if messages.has_next:
        filters['next_page'] = messages.next_num
    else:
        filters['next_page'] = None
    messages = [m.to_dict(include_profile=True, parse_timestamps=True,
                          include_transmissions=True)
                for m in messages.items]
    filters['filtered'] = filtered
    return messages, filters
