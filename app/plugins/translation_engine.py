from app import logger, rule
from app.plugins.translation.address_helper import (get_global_addresses,
                                                    get_target_addresses)
from app.plugins.translation.mask_helper import mask, unmask
from app.plugins.translation.generation_helper import choose_containerID


#-----------------------------TRANSLATION ENGINE-------------------------------#


def translate(payload, message_type, token_id, mode, exception=False, settings={}):
    # mask/unmask payload
    logger.debug('{0}ing fields: {1}'.format(mode, token_id))

    # get addresses
    address_book, stringified_address_book = get_global_addresses(payload)

    # substitute
    mask_paths = rule.substitutes(message_type)
    for path in mask_paths:
        payload = substitute(payload, path, token_id, mode,
                             address_book, stringified_address_book,
                             message_type, exception)

    # sanitize
    safe_paths = rule.sanitizers(message_type)
    for path in safe_paths:
        payload = sanitize(payload, path, token_id, mode,
                           address_book, stringified_address_book,
                           message_type, exception)

    logger.debug('finished {0}ing fields: {1}'.format(mode, token_id))
    return payload


#---------------------------SUBSTITUTION MANAGER-------------------------------#


def substitute(payload, path, token_id, mode, address_book,
               stringified_address_book, message_type, exception):
    addresses = get_target_addresses(payload, path, mode, address_book,
                                     stringified_address_book, 'substitute')
    for address in addresses:
        if mode == 'mask':
            payload = mask(address, payload, token_id, 'substitute',
                           message_type, exception)
        elif mode == 'unmask':
            payload = unmask(address, payload, token_id, 'substitute',
                             message_type)
    return payload


#---------------------------SANITIZATION MANAGER-------------------------------#


def sanitize(payload, path, token_id, mode, address_book,
             stringified_address_book, message_type, exception):
    addresses = get_target_addresses(payload, path, mode, address_book,
                                     stringified_address_book, 'sanitize')
    for address in addresses:
        if mode == 'mask':
            payload = mask(address, payload, token_id, 'sanitize',
                           message_type, exception)
        elif mode == 'unmask':
            payload = unmask(address, payload, token_id, 'sanitize',
                             message_type)
    return payload

-
#------------------------------INJECTION MANAGER-------------------------------#


def inject(payload, path, key, value):
    address_book, stringified_address_book = get_global_addresses(payload)
    addresses = get_target_addresses(payload, path, 'inject', address_book,
                                     stringified_address_book, 'injection')
    for address in addresses:
        payload = insert(address, payload, key, value)
    return payload, collection


#-----------------------------WITHDRAWAL MANAGER-------------------------------#


#---------------------------CONFIGURATION HANDLER------------------------------#


def handle_southbound_containerId(payload, settings, message_type):
    if 'containerId' in settings.keys():
        if settings['containerId']['type'] == 'first':
            return payload
        elif settings['containerId']['type'] == 'random':
            data_paths = rule.custom_data(message_type)
            for path in data_paths:
                payload = inject(
                    payload, path, 'containerIdGeneration', 'enabled')
        elif settings['containerId']['type'] == 'scanAtInduct':
            data_paths = rule.custom_data(message_type)
            for path in data_paths:
                payload = inject(
                    payload, path, 'containerIdGeneration', 'stubbed')
            generation_paths = rule.generations(
                message_type, 'containerID')
            for path in generation_paths:
                settings['containerId']['collection'], containerID = choose_containerID(
                    settings['containerID']['collection'])
                payload = inject(
                    payload, path, 'containerID', containerID)
    return payload, settings


def handle_northbound_containerId(payload, settings, token):
    # check settings for settings.containerId.type
    # if type == first, do nothing and return payload
    # if type == random, remove containerIdGeneration and return payload
    # if type == scanAtInduct
               # check if MaskMap exists for containerId
               # if MaskMap exists, unmask containerIds (based on rulebook)
               # if MaskMap does not exist, select oldest used container from settings.containerId.collection and make mask
               # unmask containerIds
               # return payload
    return
