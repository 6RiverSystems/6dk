import json

import requests

from app import app


def send_account_request(form):
    data = {
        'first_name': form.first_name.data,
        'last_name': form.last_name.data,
        'email': form.email.data
    }
    response = requests.post(app.config['HOME_BASE_URL']
                             + '/6dk-manager/user-request',
                             data=json.dumps(data),
                             auth=(app.config['HOME_BASE_USERNAME'],
                                   app.config['HOME_BASE_PASSWORD']),
                             timeout=2)
    try:
        msg = response.json()['message']
    except:
        msg = 'Failed to send account request. Try again later.'
    return msg
