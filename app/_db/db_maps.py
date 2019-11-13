from app.models import (User, Profile, MaskMap, Message, MessageTransmission)


def get_maps():
    return [
        {'name': 'users', 'table': User},
        {'name': 'profiles', 'table': Profile},
        {'name': 'mask-maps', 'table': MaskMap},
        {'name': 'messages', 'table': Message},
        {'name': 'message-transmissions', 'table': MessageTransmission}
    ]


def get_table(table):
    found = next(
        (mapping for mapping in get_maps()
         if mapping['name'] == table.lower()), None)
    if not found:
        return found
    else:
        return found['table']
