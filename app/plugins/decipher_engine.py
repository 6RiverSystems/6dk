import re

from app.models import MaskMap
from app import logger, rule
from app.plugins.translation_engine import substitute
from app.plugins.translation.address_helper import get_global_addresses


#--------------------------------DECIPHER ENGINE-------------------------------#


def decipher(payload, message_type):
	logger.debug('deciphering {} message'.format(message_type))
	address_book, stringified_address_book = get_global_addresses(payload)
	lookup_paths = rule.substitutes(message_type) + rule.sanitizers(message_type)
	token_list = [
					match_masked_fields(path, address_book)
					for path in lookup_paths
					]
	if all(x == token_list[0] for x in token_list):
		token = token_list[0]
	else:
		token = None
	if token:
		logger.debug('found token for {0} message {1}'.format(message_type, 
																token))
		mask_paths = rule.substitutes(message_type)
		for path in mask_paths:
			payload = substitute(payload, path, token, 'unmask', address_book, 
									stringified_address_book, message_type)
	else:
		logger.debug('could not find token for {} message'.format(message_type))
	return token, payload


def match_masked_fields(path, address_book, stringified_address_book):
	path = path['key_path']
	value_matches = [
					address_book[stringified_address_book.index(f)][-1] 
					for f in stringified_address_book 
					if re.compile('^{}$'.format(path)).match('.'.join(f[:-1]))
					]	
	map_matches = [
					MaskMap.query.filter_by(value=value).first()
					for value in value_matches
					]
	if None in map_matches and len(map_matches)>0: #if there's a mismatch
		return
	else:
		tokens = [match.token_id for match in map_matches]
		if all(x == tokens[0] for x in tokens): # if they are all the same
			return tokens[0]
		else:
			return None