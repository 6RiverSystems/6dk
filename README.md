# 6DK - 6 River Systems Development Kit

## Wiki
https://6river.atlassian.net/wiki/spaces/6RS/pages/828735489/6+River+Systems+Development+Kit+6DK

## Server Setup

### Install Dependencies
pipenv install --three <br />


### Enter Environment
pipenv shell <br/>
export FLASK_APP=6rweb.py <br />


### Initialize Database
flask db init <br />
flask db migrate <br />
flask db upgrade <br />
flask run (optional -p port #) <br />


### Populate Database with Initial User
cd testdata && curl -d@sdk-user.json -H "6Dk-Admin-Token: 09dfe030-e97d-4c59-b440-c936d212e0ab" http://localhost:5000/admin/users <br />
This will create an initial user for testing - username and password in sdk-user.json


### Login
http://localhost:5000/


### Environment Variables
SECRET_KEY <br />
SQLALCHEMY_DATABASE_URI <br />
ADMIN_TOKENS <br />
DEV_FS_BASE_URL <br />
MAX_PROFILE_COUNT <br />
ELEMENTS_PER_PAGE <br />
MAIL_SERVER <br />
MAIL_PORT <br />
MAIL_USE_TLS <br />
MAIL_PASSWORD <br />
FS_AUTH <br />


## Tests
coverage run tests.py && coverage report app/\*.py && coverage report app/\*/\*.py && coverage report app/\*/\*/\*.py && coverage html app/\*.py && coverage html app/\*/\*.py && coverage html app/\*/\*/\*.py
