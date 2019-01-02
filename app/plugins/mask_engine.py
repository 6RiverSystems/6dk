import re
import operator
from uuid import uuid4
from functools import reduce

from app import db, logger
from app.models import MaskPath, MaskMap


def mask_payload_fields(payload, message_type, token_id):
	logger.debug('masking fields: {}'.format(token_id))
	mask_paths = MaskPath.query.filter_by(message_type=message_type).all()
	for path in mask_paths:
		payload = mask_field(payload, path, token_id)
	logger.debug('finished masking fields: {}'.format(token_id))
	return payload


def mask_field(payload, path, token_id):
	replacement_field_addresses = get_target_field_addresses(payload, path)
	for address in replacement_field_addresses:
		payload = make_replacement(address, payload, token_id)
	db.session.commit()
	return payload


def get_by_path(root, items):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)

def set_by_path(root, items, value):
    """Set a value in a nested object in root by item sequence."""
    get_by_path(root, items[:-1])[items[-1]] = value



def make_replacement(address, payload, token_id):
	external_value = get_by_path(payload, address)
	field_name = address[-1]
	exist = MaskMap.query.filter_by(
									token_id=token_id,
									field_name=field_name,
									external_value=external_value
									).first()
	if exist==None:
		value = str(uuid4())	
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


def get_target_field_addresses(payload, path):
	flattened_dict = [x for x in flatten_dict(payload)]
	stringified_flattened_dict = [
									[str(y) for y in x] 
									for x in flattened_dict]
	path = path.key_path.replace('#','\d+')
	logger.debug('searching {0} addresses to find match for {1}'.format(
															len(flattened_dict),
															path
															))
	fields_to_replace = [
						flattened_dict[stringified_flattened_dict.index(f)][:-1] 
						for f in stringified_flattened_dict 
						if re.compile('^{}$'.format(path)).match('.'.join(f[:-1]))]
	logger.debug('found {0} fields to replace based on {1} address'.format(
															len(fields_to_replace),
															path
															))
	return fields_to_replace


def flatten_dict(indict, pre=None):
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