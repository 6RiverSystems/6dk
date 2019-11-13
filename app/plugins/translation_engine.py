from app import logger, rule
from app.plugins.translation.address_helper import (get_global_addresses,
                                                    get_target_addresses)
from app.plugins.translation.mask_helper import mask, unmask


#-----------------------------TRANSLATION ENGINE----------------------------#


def translate(payload, message_type, token_id, mode, exception=False):
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


#---------------------------SUBSTITUTION MANAGER----------------------------#


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


#---------------------------SANITIZATION MANAGER----------------------------#


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
