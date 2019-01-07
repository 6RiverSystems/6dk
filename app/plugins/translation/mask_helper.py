from uuid import uuid4

from app import db, logger, rule
from app.models import MaskMap
from app.plugins.translation.payload_manipulator import get_by_path, set_by_path


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
