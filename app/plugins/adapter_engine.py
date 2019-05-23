import requests

from app import rule, logger


def adapt_payload(original_payload, message_settings):
	logger.debug('adapting {0} {1} payload'.format(message_settings['name'],
												 message_settings['format']))
	adaptation_rules = rule.get_transporter_rules(
								message_settings['name'], 
								message_settings['transport'], 
								message_settings['format']
								)
	if adaptation_rules['adapter_required']:
		try:
			return requests.post(adaptation_rules['adapter_endpoint'],
								headers=adaptation_rules['adapter_headers'],
								data=original_payload).json()
		except:
			logger.debug('unable to adapt {0} {1} payload'.format(
												message_settings['name'],
												message_settings['format']))
			return {}
	else:
		return original_payload
