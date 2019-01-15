import requests
from flask import Response

from app import app, logger


def _proxy(request, data, destination, additional_headers=None, to_fs=False):
	logger.debug('forwarding to server: {}'.format(destination))
	headers = {key: value for (key, value) in request.headers if key != 'Host'}
	if to_fs:
		additional_headers = {'Authorization': 'Basic '+app.config['FS_AUTH']}
	if additional_headers:
		headers = {**headers, **additional_headers}
	resp = requests.request(
		method=request.method,
		url=destination,
		headers=headers,
		data=data,
		cookies=request.cookies,
		allow_redirects=False)
	excluded_headers = ['content-encoding', 'content-length', 
						'transfer-encoding', 'connection']
	headers = [(name, value) for (name, value) in resp.raw.headers.items()
				if name.lower() not in excluded_headers]

	return Response(resp.content, resp.status_code, headers)