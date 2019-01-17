from unittests.base import sixDKTests


class DbTests(sixDKTests):


	def testDbUserCheckPasswordSuccess(self):
		"""test database User check password success
		
		database should accept correct password
		"""
		return


	def testDbUserCheckPasswordFail(self):
		"""test database User check password fail
		
		database should reject incorrect password
		"""
		return


	def testDbUserSetPassword(self):
		"""test database User set password
		
		database should update password hash
		"""
		return


	def testDbUserLoadProfiles(self):
		"""test database User load profiles
		
		database should return active user profiles
		"""
		return


	def testDbUserLoadDeletedProfiles(self):
		"""test database User load deleted profiles
		
		database should return deleted user profiles
		"""
		return


	def testDbUserGetActiveProfile(self):
		"""test database get active profile
		
		database should return active profile for user
		"""
		return


	def testDbUserOwnsTokenTrue(self):
		"""test database User own token success
		
		database should acknowledge if a user owns a token
		"""
		return


	def testDbUserOwnsTokenFalse(self):
		"""test database User own token failure
		
		database should acknowledge if a user does not own a token
		"""
		return


	def testDbUserGetNewMessages(self):
		"""test database User get messages
		
		database should return messages for user
		"""
		return


	def testDbUserResetPasswordTokens(self):
		"""test database User reset password tokens
		
		database should successfully create and check password reset tokens
		"""
		return


	def testDbUserForwardProfileTokens(self):
		"""test database User forward profile tokens
		
		database should successfully create and check forward profile tokens
		"""
		return


	def testDbUserDict(self):
		"""test database User dictionary
		
		database should return correct User dictionary object
		"""
		return


	def testDbProfileIsActiveTrue(self):
		"""test database Profile is active success
		
		database should correctly acknowledge if a profile is active
		"""
		return


	def testDbProfileIsActiveFalse(self):
		"""test database Profile is active fail
		
		database should correctly acknowledge if a profile is inactive
		"""
		return


	def testDbProfileFindOwnerSuccess(self):
		"""test database Profile find owner success
		
		database should correctly return owner of a profile
		"""
		return


	def testDbProfileFindOwnerFail(self):
		"""test database Profile find owner success
		
		database should correctly return None for ownerless profiles
		"""
		return


	def testDbProfileDict(self):
		"""test database Profile dictionary
		
		database should return correct Profile dictionary object
		"""
		return


	def testDbMaskMapDict(self):
		"""test database MaskMap dictionary
		
		database should return correct MaskMap dictionary object
		"""
		return


	def testDbMessageGetReplays(self):
		"""test database message replays
		
		database should return message replays object
		"""
		return


	def testDbMessageDict(self):
		"""test database Message dictionary
		
		database should return correct Message dictionary object
		"""
		return


	def testDBMessageTransmissionDict(self):
		"""test database MessageTransmission dictionary
		
		database should return correct MessageTransmission dictionary object
		"""
		return