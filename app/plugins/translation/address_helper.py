import re

from app import logger
from app.plugins.translation.payload_manipulator import flatten_dict


def get_global_addresses(payload):
    # get global addresses
    address_book = [x for x in flatten_dict(payload)]
    stringified_address_book = [
        [str(y) for y in x]
        for x in address_book]
    return address_book, stringified_address_book


def get_target_addresses(payload, path, mode, address_book,
                         stringified_address_book, func_name):

    logger.debug('{0}: searching {1} addresses to find match for {2}'.format(
        func_name,
        len(address_book),
        path
    ))
    if mode == 'mask':
        path = path['key_path']
        fields_to_replace = [
            address_book[stringified_address_book.index(f)][:-1]
            for f in stringified_address_book
            if re.compile('^{}$'.format(path)).match('.'.join(f[:-1]))]
    elif mode == 'unmask':
        path = path['field_name']
        fields_to_replace = [
            address_book[stringified_address_book.index(f)][:-1]
            for f in stringified_address_book
            if f[-2] == path]
    logger.debug('{0}: found {1} fields to {2} based on {3}'.format(
        len(fields_to_replace),
        func_name,
        mode,
        path
    ))
    return fields_to_replace
