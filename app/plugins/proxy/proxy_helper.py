import requests
from flask import Response

from app import logger


def _proxy(request, data, destination):
	logger.debug('forwarding to server: {}'.format(destination))
	resp = requests.request(
		method=request.method,
		url=destination,
		headers={key: value for (key, value) in request.headers if key != 'Host'},
		data=data,
		cookies=request.cookies,
		allow_redirects=False)
	excluded_headers = ['content-encoding', 'content-length', 
						'transfer-encoding', 'connection']
	headers = [(name, value) for (name, value) in resp.raw.headers.items()
				if name.lower() not in excluded_headers]

	return Response(resp.content, resp.status_code, headers)