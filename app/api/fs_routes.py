import copy

from flask import request, jsonify

from app import app, logger, rule
from app.models import Profile
from app.plugins.auth_helper import user_token_validation
from app.plugins.translation_engine import translate
from app.plugins.proxy_engine import serve_proxy
from app.plugins.adapter_engine import adapt_payload
from app.plugins.general_helper import verify_first_pick_wave, enabled_message


@app.route('/<mode>/<version>/pick-waves', methods=['POST'])
@app.route('/<mode>/wis-southbound/<version>/pick-waves', methods=['POST'])
@user_token_validation
def receive_southbound(mode, version):
    token = request.headers['6Dk-Token']
    if enabled_message(token, 'pick-waves'):
        profile = Profile.query.get(token).to_dict()
        settings = next(
            message
            for message in profile['data']['southbound_messages']
            if message['name'] == 'pick-waves'
        )
        if settings['format'].lower() == 'json':
            original_payload = request.get_json(force=True) or {}
            payload = copy.deepcopy(original_payload)
        else:
            original_payload = request.get_data()
            payload = adapt_payload(original_payload, settings, 'southbound')
        logger.debug(
            'receiving pick-waves message: {}'.format(original_payload))
        if mode == 'dev':
            masked_data = translate(payload, 'pick-waves', token, 'mask')
        elif mode == 'exp':
            masked_data = translate(payload, 'pick-waves', token, 'mask',
                                    exception=True)
        else:
            return jsonify({'message': 'bad request'}), 400
        response = serve_proxy(settings,
                               original_payload, masked_data,
                               'pick-waves',
                               '/{0}/wis-southbound/{1}/pick-waves'.format(
                                   mode, version),
                               token, app.config['DEV_FS_BASE_URL'] +
                               '/cfs/wis-southbound/{}/pick-waves'.format(
                                   version),
                               request)
        verify_first_pick_wave(token)
        return response
    else:
        return jsonify(
            {'message': 'pick-waves message type is not enabled'}), 405


@app.route('/dev/wis-order-update/v1/<message_type>', methods=['POST'])
@user_token_validation
def receive_order_update(message_type):
    """
    only attempt to get JSON if token says transport is JSON via HTTPS
    otherwise use adapter
    """
    token = request.headers['6Dk-Token']
    if enabled_message(token, message_type):
        if message_type in rule.get_messages_list('order_update'):
            if message_type == 'container-cancels':
                uri = 'ContainerCancels'
            elif message_type == 'group-updates':
                uri = 'GroupUpdates'
            else:
                uri = ''
            original_payload = request.get_json(force=True) or {}
            payload = copy.deepcopy(original_payload)
            logger.debug('receiving {0} message: {1}'.format(
                message_type, payload))

            profile = Profile.query.get(token).to_dict()
            settings = next(
                message
                for message in profile['data']['southbound_messages']
                if message['name'] == 'pick-waves'
            )
            masked_data = translate(
                payload, message_type, token, 'mask', exception=True)
            response = serve_proxy(settings,
                                   original_payload, masked_data,
                                   message_type,
                                   '/dev/wis-order-update/v1/{}'.format(
                                       message_type),
                                   token, app.config['DEV_FS_BASE_URL'] +
                                   '/cfs/wis-order-update/v1/{}'.format(
                                       uri),
                                   request)
            return response
        else:
            return jsonify({'message': 'unknown message type'}), 404
    else:
        return jsonify(
            {'message': '{} message type is not enabled'.format(
                message_type)}), 405
