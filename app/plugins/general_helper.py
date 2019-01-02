

def check_for_keys(keys, dict):
	missing = [key for key in keys if key not in dict.keys()]
	if len(missing)==0:
		return True, []
	else:
		return False, missing