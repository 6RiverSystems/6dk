import dateparser

from app import app
from app.models import Message, Profile 


def filter_feed(filters, user_profiles, return_data=False, order="desc"):
	messages = Message.query
	filtered = False
	if len(filters['message_type'])>0:
		messages = messages.filter(
							Message.message_type.in_(filters['message_type']))
		filtered = True

	if len(filters['profile'])>0:
		messages = messages.filter(Message.token_id.in_(filters['profile']))
		profiles = Profile.query.filter(
									Profile.token_id.in_(filters['profile'])
									).all()
		filters['profile_names'] = [p.to_dict()['data']['friendly_name'] 
									for p in profiles]
		filtered = True
	else:
		token_ids = [
						profile['token_id'] 
						for profile in user_profiles
					]
		messages = messages.filter(Message.token_id.in_(token_ids))
		filters['profile_names'] = ['all profiles']

	try:
		start = dateparser.parse(filters['sent_after'])
		messages = messages.filter(Message.updated>=start)
		filtered = True
	except:
		pass

	try:
		end = dateparser.parse(filters['sent_before'])
		messages = messages.filter(Message.updated<=end)
		filtered = True
	except:
		pass

	if filters['q']:
		if len(filters['q'])>=3:
			messages = messages.filter(
								Message.unmasked_data.like(
												'%{}%'.format(filters['q'])))
			filtered = True
	filters['count'] = messages.count()
	
	if order=='desc':
		messages = messages.order_by(
								Message.updated.desc()
								)
	elif order=='asc':
		messages = messages.order_by(
								Message.updated.asc()
								)
	
	data = [m.to_dict(include_profile=True, parse_timestamps=True,
							include_transmissions=True) 
				for m in messages.all()]
	filters['transmissions'] = sum([m['transmissions_info']['count'] for m in data])
	if return_data:
		return data, filters
	messages = messages.paginate(
								filters['page'], 
								app.config['ELEMENTS_PER_PAGE'], 
								False)
	filters['has_next'] = messages.has_next
	if messages.has_next:
		filters['next_page'] = messages.next_num
	else:
		filters['next_page'] = None
	messages = [m.to_dict(include_profile=True, parse_timestamps=True, 
							include_transmissions=True) 
				for m in messages.items]
	filters['filtered'] = filtered
	return messages, filters