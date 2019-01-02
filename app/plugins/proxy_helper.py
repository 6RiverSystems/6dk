import requests
from flask import Response

from app import logger


def _proxy(request, destination):
	logger.debug('forwarding to server: {}'.format(destination))
	resp = requests.request(
		method=request.method,
		url=request.url.replace(request.host_url, destination),
		headers={key: value for (key, value) in request.headers if key != 'Host'},
		data=request.get_data(),
		cookies=request.cookies,
		allow_redirects=False)
	#unmask here before making the response object
	excluded_headers = ['content-encoding', 'content-length', 
						'transfer-encoding', 'connection']
	headers = [(name, value) for (name, value) in resp.raw.headers.items()
				if name.lower() not in excluded_headers]

	return Response(resp.content, resp.status_code, headers)