import copy
import subprocess
import os
import json

from flask import jsonify, request

from app import app, logger, rule
from app.models import Message, Profile
from app.plugins.adapter_engine import adapt_payload
from app.plugins.decipher_engine import decipher
from app.plugins.proxy_engine import wms_forwarder
from app.plugins.proxy_engine import wms_repeater
from app.plugins.general_helper import enabled_message


@app.route('/wms/<message_type>', methods=['POST'])
def receive_wms_request(message_type):
    """
    only attempt to get JSON if token says transport is JSON via HTTPS
    otherwise use adapter
    """
    valid_messages = rule.get_messages_list('northbound')
    if message_type in valid_messages:
        original_payload = request.get_json(force=True) or {}
        payload = copy.deepcopy(original_payload)
        logger.debug('receiving {0} message: {1}'.format(
            message_type, payload))
        token, unmasked_data = decipher(payload, message_type)
        if token:
            if enabled_message(token, message_type):
                profile = Profile.query.get(token).to_dict()
                settings = next(
                    message
                    for message in profile['data']['northbound_messages']
                    if message['name'] == message_type
                )
                if settings['format'].lower() != 'json':
                    unmasked_data = adapt_payload(json.dumps(
                        unmasked_data), settings, 'northbound')
                return wms_forwarder(unmasked_data,
                                     original_payload, message_type,
                                     '/wms/{}'.format(message_type), token,
                                     request, message_format=settings['format'])
            else:
                return jsonify(
                    {'message': 'accepted but origin wms is not configured to receive {}'.format(
                        message_type)})
        else:
            return jsonify({'message': 'accepted but origin wms not found'})
    else:
        return jsonify({'message': 'unknown message type'}), 404


@app.route('/wms/replay/<message_id>/<token_id>', methods=['POST'])
def resend_to_wms(message_id, token_id):
    message = Message.query.filter_by(id=message_id).first().to_dict()
    profile = Profile.query.filter_by(token_id=token_id).first().to_dict()
    message_settings = next(msg
                            for msg in profile['data']['northbound_messages']
                            if msg['name'] == message['message_type'])
    with open('{}.txt'.format(message['id']), 'w') as f:
        f.write(message['unmasked_data'])
    args = ["curl", "-vvv"]
    for header in message_settings['wms_headers']:
        args += ["-H", header]

    args += ["-d@{}.txt".format(message['id']), "-m", "2.0"]
    args += ["{0}:{1}/{2}".format(
        message_settings['wms_host'],
        message_settings['wms_port'],
        message_settings['wms_path'],
    )]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    os.remove('{}.txt'.format(message['id']))
    wms_repeater(message_id)
    replays = Message.get_replays(message_id)
    replay_text = '{} transmission'.format(replays['count'])
    if replays['count'] != 1:
        replay_text += 's'
    return jsonify({'html': '{}'.format(out.decode('utf-8')),
                    'replays': replays,
                    'replay_text': replay_text})


@app.route('/wms/receiver', methods=['POST'])
def wms_receiver():
    return jsonify({'message': 'OK'})
