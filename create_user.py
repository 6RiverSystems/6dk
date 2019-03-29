import requests
import json

while True:
    first_name = input('first name: ')
    last_name = input('last name: ')
    email = input('email: ')

    r = requests.post('https://sixdk.6river.tech/admin/users?welcome=1',
                      data=json.dumps({
                          'first_name': first_name,
                          'last_name': last_name,
                          'email': email
                      }),
                      headers={
                          'Content-Type': 'application/json',
                          '6Dk-Admin-Token': '09dfe030-e97d-4c59-b440-c936d212e0ab'
                      })
    print(r.status_code)
