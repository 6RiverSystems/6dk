import json

from app import db
from app.plugins.translation.payload_manipulator import (
    flatten_dict, set_by_path)


def model_data_updater(orig_object, template):
    object_data = json.loads(orig_object.data)
    object_addresses = [x for x in flatten_dict(object_data)]
    to_add = []
    template_addresses = [x for x in flatten_dict(template)]

    for addr in template_addresses:
        exist = next((address for address in object_addresses
                      if address[:-1] == addr[:-1]), None)
        if not exist:
            to_add.append(addr)

    if len(to_add) == 0:
        return orig_object
    else:
        try:
            for addr in to_add:
                set_by_path(object_data, addr[:-1], addr[-1])
            orig_object.data = json.dumps(object_data)
        except:
            orig_object.data = json.dumps(template)
        db.session.commit()
        return orig_object
