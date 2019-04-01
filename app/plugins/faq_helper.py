import requests
import json

from app import app, dk_faqs, logger


def get_faqs(method):
    if method == 'GET':
        try:
            faqs = json.loads(
                requests.get(
                    app.config['HOME_BASE_URL'] +
                    '/persistence/api/v1/load/6dk-faqs',
                    auth=(
                        app.config['HOME_BASE_USERNAME'],
                        app.config['HOME_BASE_PASSWORD'])
                ).json()['data'])
            faqs = sorted(faqs, key=lambda k: k['Q'])
            logger.info('updating dk faqs')
            dk_faqs.update(faqs)
        except:
            logger.info('failed to fetch dk faqs')
            faqs = []
    else:
        logger.info('using saved dk faqs')
        return dk_faqs.get()
    return faqs
