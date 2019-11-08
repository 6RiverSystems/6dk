from unittests.base import sixDKTests

from app.models import User, Profile
from app.plugins.general_helper import check_for_keys


class ApiAdminTests(sixDKTests):

    def testCreateUserSuccessResponse(self):
        """test Admin API success response for creating a new user

        API should return payload with user object
        """
        response = self.app.post('/admin/users',
                                 data=self.get_payload('sdk-user.json'),
                                 headers=self.admin_header())
        self.assertTrue(check_for_keys(['id', 'email', 'first_name',
                                        'last_name', 'created', 'updated',
                                        'data'],
                                       response.json)[0])

    def testCreateUserSuccessDatabase(self):
        """test Admin API database update for creating a new user

        User table should be populated with user
        """
        self.app.post('/admin/users',
                      data=self.get_payload('sdk-user.json'),
                      headers=self.admin_header())
        self.assertTrue(User.query.count() == 1
                        and User.query.first().email == 'rivs@6river.com')

    def testCreateUserMissingTokenResponse(self):
        """test Admin API missing token response for creating a new user

        API should return error message
        """
        response = self.app.post('/admin/users',
                                 data=self.get_payload('sdk-user.json'),
                                 )
        self.assertTrue(response.json['message']
                        == 'no 6Dk-Admin-Token supplied')

    def testCreateUserMissingTokenDatabase(self):
        """test Admin API missing token database update for creating a new user

        API should not create a new user
        """
        self.app.post('/admin/users',
                      data=self.get_payload('sdk-user.json'),
                      )
        self.assertTrue(User.query.count() == 0)

    def testCreateUserWrongTokenResponse(self):
        """test Admin API wrong token response for creating a new user

        API should return error message
        """
        response = self.app.post('/admin/users',
                                 data=self.get_payload('sdk-user.json'),
                                 headers={'6Dk-Admin-Token': 'bad-token-1234'}
                                 )
        self.assertTrue(response.json['message']
                        == '6Dk-Admin-Token not found')

    def testCreateUserWrongTokenDatabase(self):
        """test Admin API wrong token database update for creating a new user

        API should not create a new user
        """
        self.app.post('/admin/users',
                      data=self.get_payload('sdk-user.json'),
                      headers={'6Dk-Admin-Token': 'bad-token-1234'}
                      )
        self.assertTrue(User.query.count() == 0)

    def testCreateUserMissingEmailResponse(self):
        """test Admin API missing email response for creating a new user

        API should return error message
        """
        data = self.remove_keys(self.get_payload('sdk-user.json'),
                                keys=['email'])
        response = self.app.post('/admin/users',
                                 data=data,
                                 headers=self.admin_header()
                                 )
        self.assertTrue(response.json['message'] == 'missing email')

    def testCreateUserMissingEmailDatabase(self):
        """test Admin API missing email response for creating a new user

        API should not create a new user
        """
        data = self.remove_keys(self.get_payload('sdk-user.json'),
                                keys=['email'])
        self.app.post('/admin/users',
                      data=data,
                      headers=self.admin_header()
                      )
        self.assertTrue(User.query.count() == 0)

    def testCreateUserDuplicateEmailResponse(self):
        """test Admin API duplicate email response for creating a new user

        API should return error message
        """
        self.create_user()
        response = self.app.post('/admin/users',
                                 data=self.get_payload('sdk-user.json'),
                                 headers=self.admin_header())
        self.assertTrue(
            response.json['message'] == 'User for email, rivs@6river.com, already exists')

    def testCreateUserDuplicateEmailDatabase(self):
        """test Admin API duplicate email response for creating a new user

        API should not create a new user
        """
        self.create_user()
        self.app.post('/admin/users',
                      data=self.get_payload('sdk-user.json'),
                      headers=self.admin_header())
        self.assertTrue(User.query.count() == 1)

    def testCreateProfileSuccessResponse(self):
        """test Admin API success response for creating a new profile

        API should return payload with profile object
        """
        self.create_user()
        response = self.app.post('/admin/profiles',
                                 data='{"email": "rivs@6river.com"}',
                                 headers=self.admin_header())
        self.assertTrue(
            check_for_keys(['token_id', 'user', 'created', 'updated',
                                        'data'], response.json)[0]
            and check_for_keys(['friendly_name', 'active',
                                'northbound_messages',
                                'southbound_messages'],
                               response.json['data'])[0])

    def testCreateProfileSuccessDatabase(self):
        """test Admin API database update for creating a new profile

        Profile table should be populated with profile
        """
        user = self.create_user()
        self.app.post('/admin/profiles',
                      data='{"email": "rivs@6river.com"}',
                      headers=self.admin_header())
        self.assertTrue(Profile.query.count() == 1
                        and Profile.query.first().user == user['id'])

    def testCreateProfileMissingTokenResponse(self):
        """test Admin API missing token response for creating a new profile

        API should return error message
        """
        self.create_user()
        response = self.app.post('/admin/profiles',
                                 data='{"email": "rivs@6river.com"}')
        self.assertTrue(response.json['message']
                        == 'no 6Dk-Admin-Token supplied')

    def testCreateProfileMissingTokenDatabase(self):
        """test Admin API missing token database update
        for creating a new profile

        API should not create profile
        """
        self.create_user()
        self.app.post('/admin/profiles',
                      data='{"email": "rivs@6river.com"}')
        self.assertTrue(Profile.query.count() == 0)

    def testCreateProfileWrongTokenResponse(self):
        """test Admin API wrong token response
        for creating a new profile

        API should return error message
        """
        self.create_user()
        response = self.app.post('/admin/profiles',
                                 data='{"email": "rivs@6river.com"}',
                                 headers={'6Dk-Admin-Token': 'bad-token-1234'}
                                 )
        self.assertTrue(response.json['message']
                        == '6Dk-Admin-Token not found')

    def testCreateProfileWrongTokenDatabase(self):
        """test Admin API wrong token database update
        for creating a new profile

        API should not create profile
        """
        self.create_user()
        self.app.post('/admin/profiles',
                      data='{"email": "rivs@6river.com"}',
                      headers={'6Dk-Admin-Token': 'bad-token-1234'}
                      )
        self.assertTrue(Profile.query.count() == 0)

    def testCreateProfileMissingEmailResponse(self):
        """test Admin API missing email response for creating a new profile

        API should return error message
        """
        self.create_user()
        response = self.app.post('/admin/profiles',
                                 data='{"foo": "bar"}',
                                 headers=self.admin_header())
        self.assertTrue(response.json['message'] == 'missing email')

    def testCreateProfileMissingEmailDatabase(self):
        """test Admin API missing email database update
        for creating a new profile

        API should not create profile
        """
        self.create_user()
        self.app.post('/admin/profiles',
                      data='{"foo": "bar"}',
                      headers=self.admin_header())
        self.assertTrue(Profile.query.count() == 0)

    def testCreateProfileUnknownEmailResponse(self):
        """test Admin API unknown email response for creating a new profile

        API should return error message
        """
        self.create_user()
        response = self.app.post('/admin/profiles',
                                 data='{"email": "rivs2@6river.com"}',
                                 headers=self.admin_header())
        self.assertTrue(response.json['message'] ==
                        'user not found for email: rivs2@6river.com')

    def testCreateProfileUnknownEmailDatabase(self):
        """test Admin API unknown email database update
        for creating a new profile

        API should not create profile
        """
        self.create_user()
        self.app.post('/admin/profiles',
                      data='{"email": "rivs2@6river.com"}',
                      headers=self.admin_header())
        self.assertTrue(Profile.query.count() == 0)

    def testModProfileSuccessResponse(self):
        """test Admin API response for updating a profile

        API should return Profile object
        """
        user, profile = self.create_user(include_profile=True)
        response = self.app.put(
            '/admin/profiles/{}'.format(profile['token_id']),
            data='{"data":{"foo":"bar"}}',
            headers=self.admin_header())
        self.assertTrue(
            check_for_keys(['token_id', 'user', 'created', 'updated',
                                        'data'], response.json)[0]
            and check_for_keys(['foo'],
                               response.json['data'])[0])

    def testModProfileSuccessDatabase(self):
        """test Admin API database update for updating a profile

        API should modify Profile.data
        """
        user, profile = self.create_user(include_profile=True)
        self.app.put('/admin/profiles/{}'.format(profile['token_id']),
                     data='{"data":{"foo":"bar"}}',
                     headers=self.admin_header())
        self.assertTrue('foo' in Profile.query.first().to_dict()['data'].keys()
                        and Profile.query.count() == 1)

    def testModProfileMissingTokenResponse(self):
        """test Admin API missing token response for updating a profile

        API should return error message
        """
        user, profile = self.create_user(include_profile=True)
        response = self.app.put(
            '/admin/profiles/{}'.format(profile['token_id']),
            data='{"data":{"foo":"bar"}}')
        self.assertTrue(response.json['message']
                        == 'no 6Dk-Admin-Token supplied')

    def testModProfileMissingTokenDatabase(self):
        """test Admin API missing token database update for updating a profile

        API should not modify Profile.data
        """
        user, profile = self.create_user(include_profile=True)
        self.app.put('/admin/profiles/{}'.format(profile['token_id']),
                     data='{"data":{"foo":"bar"}}')
        self.assertTrue(Profile.query.first().to_dict() == profile)

    def testModProfileWrongTokenResponse(self):
        """test Admin API wrong token response for updating a profile

        API should return error message
        """
        user, profile = self.create_user(include_profile=True)
        response = self.app.put(
            '/admin/profiles/{}'.format(profile['token_id']),
            data='{"data":{"foo":"bar"}}',
            headers={'6Dk-Admin-Token': 'bad-token-1234'})
        self.assertTrue(response.json['message']
                        == '6Dk-Admin-Token not found')

    def testModProfileWrongTokenDatabase(self):
        """test Admin API wrong token database update for updating a profile

        API should not modify Profile.data
        """
        user, profile = self.create_user(include_profile=True)
        self.app.put('/admin/profiles/{}'.format(profile['token_id']),
                     data='{"data":{"foo":"bar"}}',
                     headers={'6Dk-Admin-Token': 'bad-token-1234'})
        self.assertTrue(Profile.query.first().to_dict() == profile)

    def testModProfileMissingDataResponse(self):
        """test Admin API missing data response for updating a profile

        API should return error message
        """
        user, profile = self.create_user(include_profile=True)
        response = self.app.put(
            '/admin/profiles/{}'.format(profile['token_id']),
            data='{"foo":"bar"}',
            headers=self.admin_header())
        self.assertTrue(response.json['message'] == 'missing data')

    def testModProfileMissingDataDatabase(self):
        """test Admin API missing data database update for updating a profile

        API should not modify Profile.data
        """
        user, profile = self.create_user(include_profile=True)
        self.app.put('/admin/profiles/{}'.format(profile['token_id']),
                     data='{"foo":"bar"}',
                     headers=self.admin_header())
        self.assertTrue(Profile.query.first().to_dict() == profile)

    def testModProfileWrongDataTypeResponse(self):
        """test Admin API wrong data data type response for updating a profile

        API should return error message
        """
        user, profile = self.create_user(include_profile=True)
        response = self.app.put(
            '/admin/profiles/{}'.format(profile['token_id']),
            data='{"data":123}',
            headers=self.admin_header())
        self.assertTrue(response.json['message'] == 'data must be an object')

    def testModProfileWrongDataTypeDatabase(self):
        """test Admin API wrong data data type database update
        for updating a profile

        API should not modify Profile.data
        """
        user, profile = self.create_user(include_profile=True)
        self.app.put(
            '/admin/profiles/{}'.format(profile['token_id']),
            data='{"data":123}',
            headers=self.admin_header())
        self.assertTrue(Profile.query.first().to_dict() == profile)

    def testModProfileUnknownProfileResponse(self):
        """test Admin API unknown profile response for updating a profile

        API should return error message
        """
        user, profile = self.create_user(include_profile=True)
        response = self.app.put('/admin/profiles/foo',
                                data='{"data":{"foo":"bar"}}',
                                headers=self.admin_header())
        self.assertTrue(response.json['message'] == 'profile not found')

    def testDeleteProfileSuccessResponse(self):
        """test Admin API success response for deleting a profile

        API should return a success message
        """
        user, profile = self.create_user(include_profile=True)
        response = self.app.delete(
            '/admin/profiles/{}'.format(profile['token_id']),
            data="{}",
            headers=self.admin_header())
        self.assertTrue(response.json['message'] == 'profile deleted')

    def testDeleteProfileSuccessDatabase(self):
        """test Admin API success database update for deleting a profile

        API should return a success message
        """
        user, profile = self.create_user(include_profile=True)
        self.app.delete('/admin/profiles/{}'.format(profile['token_id']),
                        data="{}",
                        headers=self.admin_header())
        self.assertTrue(Profile.query.count() == 1
                        and Profile.query.first().deleted is True)
