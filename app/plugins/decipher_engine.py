from app.models import MaskMap
from app import logger, rule
from app.plugins.translation_engine import substitute
from app.plugins.translation.address_helper import get_global_addresses


def decipher(payload, message_type):
	logger.debug('deciphering {} message'.format(message_type))
	address_book, stringified_address_book = get_global_addresses(payload)
	lookup_paths = rule.substitutes(message_type) + rule.sanitizers(message_type)
	token_list = [
					match_masked_fields(path, address_book, 
									stringified_address_book)
					for path in lookup_paths
					]
	token_list = [token for token in token_list if token != 'not-found']
	if all(x == token_list[0] for x in token_list):
		token = token_list[0]
	else:
		token = None
	if token:
		logger.debug('found token for {0} message {1}'.format(message_type, 
																token))
		mask_paths = rule.substitutes(message_type) + rule.sanitizers(message_type)
		for path in mask_paths:
			payload = substitute(payload, path, token, 'unmask', address_book, 
									stringified_address_book, message_type)
	else:
		logger.debug('could not find token for {} message'.format(message_type))
	return token, payload


def match_masked_fields(path, address_book, stringified_address_book):
	path = path['field_name']
	value_matches = [
					address_book[stringified_address_book.index(f)][-1] 
					for f in stringified_address_book 
					if f[-2] == path
					]	
	map_matches = [
					MaskMap.query.filter_by(value=value).first()
					for value in value_matches
					]
	map_matches = [match for match in map_matches if match != None]
	if len(map_matches)>0:
		tokens = [match.token_id for match in map_matches]
		if all(x == tokens[0] for x in tokens): # if they are all the same
			return tokens[0]		
	else:
		return 'not-found'