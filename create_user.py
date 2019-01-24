import requests
import json

while True:
	first_name = input('first name: ')
	last_name = input('last name: ')
	email = input('email: ')

	r = requests.post('http://sdk-roku.herokuapp.com/admin/users?welcome=1',
					headers={
								'Content-Type': 'application/json',
								'6Dk-Admin-Token': '09dfe030-e97d-4c59-b440-c936d212e0ab'
							})
	print(r.status_code)