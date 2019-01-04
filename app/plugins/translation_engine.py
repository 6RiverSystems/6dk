import re
import operator
from uuid import uuid4
from functools import reduce

from app import db, logger, rule
from app.models import MaskMap, SafeMap


#------------------------------------HELPERS-----------------------------------#


def get_by_path(root, items):
    #Access a nested object in root by item sequence.
    return reduce(operator.getitem, items, root)


def set_by_path(root, items, value):
    #Set a value in a nested object in root by item sequence.
    get_by_path(root, items[:-1])[items[-1]] = value


def get_target_addresses(payload, path, mode, address_book, 
						stringified_address_book, func_name):

	logger.debug('{0}: searching {1} addresses to find match for {2}'.format(
															func_name,
															len(address_book),
															path
															))
	if mode=='mask':
		path = path['key_path']
		fields_to_replace = [
							address_book[stringified_address_book.index(f)][:-1] 
							for f in stringified_address_book 
							if re.compile('^{}$'.format(path)).match('.'.join(f[:-1]))]
	elif mode=='unmask':
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


def flatten_dict(indict, pre=None):
	#convert dictionary into generator of lists of indices
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in flatten_dict(value, pre + [key]):
                    yield d
            elif isinstance(value, list):
                for v in value:
                    for d in flatten_dict(v,  pre + [key] + [value.index(v)]):
                        yield d
            else:
                yield pre + [key, value]
    elif isinstance(indict, list):
    	for value in indict:
    		for d in flatten_dict(value, pre + [value]):
    			yield d
    else:
        yield pre + [indict]


def mask(address, payload, token_id, func_name, message_type):
	#replace external values
	external_value = get_by_path(payload, address)
	field_name = address[-1]
	exist = MaskMap.query.filter_by(
									token_id=token_id,
									field_name=field_name,
									external_value=external_value
									).first()

	if exist==None:
		if func_name=='substitute':
			value = str(uuid4())
		elif func_name=='sanitize':
			value = rule.sanitize_value(message_type, field_name) 	
		set_by_path(payload, address, value)
		mask_map = MaskMap()
		mask_map.from_dict(
							dict(							
								value=value,
								token_id=token_id,
								field_name=field_name,
								external_value=external_value
								)
							)
		db.session.add(mask_map)
		db.session.commit()
		logger.debug(
			'added mask for {0}:{1}:{2}'.format(token_id,
												field_name,
												external_value
												))
	else:
		set_by_path(payload, address, exist.value)
		logger.debug(
			'skipping mask for {0}:{1}:{2} because existing mask found'.format(
																token_id,
																field_name,
																external_value
																))
	return payload


def unmask(address, payload, token_id, mode, message_type):
	#replace internal values
	internal_value = get_by_path(payload, address)
	field_name = address[-1]
	exist = MaskMap.query.filter_by(
									token_id=token_id,
									field_name=field_name,
									value=internal_value
									).first()

	if exist:
		set_by_path(payload, address, exist.external_value)
		logger.debug(
			'retrieved mask for {0}:{1}:{2}'.format(token_id,
												field_name,
												internal_value
												))
	else:
		logger.debug(
			'could not retrieve mask for {0}:{1}:{2}'.format(
																token_id,
																field_name,
																internal_value
																))
	return payload
#----------------------------------MASK ENGINE---------------------------------#


def translate(payload, message_type, token_id, mode):
	#mask/unmask payload
	logger.debug('{0}ing fields: {1}'.format(mode, token_id))
	
	#get global address books
	address_book = [x for x in flatten_dict(payload)]
	stringified_address_book = [
								[str(y) for y in x] 
								for x in address_book]

	#substitute
	mask_paths = rule.substitutes(message_type)
	for path in mask_paths:
		payload = substitute(payload, path, token_id, mode, 
							address_book, stringified_address_book, 
							message_type)

	#sanitize
	safe_paths = rule.sanitizers(message_type)
	for path in safe_paths:
		payload = sanitize(payload, path, token_id, mode,
							address_book, stringified_address_book, 
							message_type)

	logger.debug('finished {0}ing fields: {1}'.format(mode, token_id))
	return payload


#------------------------------------------------------------------------------#


def substitute(payload, path, token_id, mode, address_book, 
				stringified_address_book, message_type):
	#substitute values at paths in payload
	addresses = get_target_addresses(payload, path, mode, address_book, 
									stringified_address_book, 'substitute')
	for address in addresses:
		if mode=='mask':
			payload = mask(address, payload, token_id, 'substitute', 
							message_type)
		elif mode=='unmask':
			payload = unmask(address, payload, token_id, 'substitute', 
							message_type)
	return payload



#------------------------------------------------------------------------------#


def sanitize(payload, path, token_id, mode, address_book, 
			stringified_address_book, message_type):
	#sanitize values at paths in payload with safe values
	addresses = get_target_addresses(payload, path, mode, address_book, 
									stringified_address_book, 'sanitize')
	for address in addresses:
		if mode=='mask':
			payload = mask(address, payload, token_id, 'sanitize', 
							message_type)
		elif mode=='unmask':
			payload = unmask(address, payload, token_id, 'sanitize', 
							message_type)
	return payload


#------------------------------------------------------------------------------#


def decipher(payload, message_type):
	#query for all mask paths
	#get addresses
	#figure out which token id
	return