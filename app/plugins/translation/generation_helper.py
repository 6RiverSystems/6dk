from datetime import datetime


def choose_containerID(collection):
    collection = sorted(collection,
                        key=lambda k: (k['last_used']))
    collection[0]['last_used'] = datetime.utcnow().isoformat() + 'Z'
    return collection[0]['value'], collection
