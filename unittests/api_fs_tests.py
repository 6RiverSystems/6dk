import vcr

from unittests.base import sixDKTests


class ApiFsTests(sixDKTests):


	@vcr.use_cassette('cassettes/pick-waves-success-response.yml')
	def testPickWavesSuccessResponse(self):
		"""test FS pick-waves API success response for receiving a pick-wave

		API should return 200 OK response
		"""
		return


	@vcr.use_cassette('cassettes/pick-waves-success-database.yml')
	def testPickWavesSuccessDatabase(self):
		"""test FS pick-waves API success database update for receiving a pick-wave

		API should update Message and MessageTransmission tables with 
		pick-waves and pick-waves response records
		"""
		return


	def testPickWavesMissingTokenResponse(self):
		"""test FS pick-waves API missing token response for receiving a pick-wave

		API should return an error message
		"""
		return


	def testPickWavesMissingTokenDatabase(self):
		"""test FS pick-waves API missing token database update for receiving a pick-wave

		API should not create Message or MessageTransmission records
		"""
		return


	def testPickWavesIncorrectTokenResponse(self):
		"""test FS pick-waves API incorrect token response for receiving a pick-wave

		API should return an error message
		"""
		return


	def testPickWavesIncorrectTokenDatabase(self):
		"""test FS pick-waves API incorrect token database update for receiving a pick-wave

		API should not create Message or MessageTransmission records
		"""
		return


	@vcr.use_cassette('cassettes/exception-pick-waves-success-response.yml')
	def testExceptionPickWavesSuccessResponse(self):
		"""test FS exception pick-waves API success response for receiving a pick-wave

		API should return 200 OK response
		"""
		return


	@vcr.use_cassette('cassettes/exception-pick-waves-success-database.yml')
	def testExceptionPickWavesSuccessDatabase(self):
		"""test FS exception pick-waves API success database update for receiving a pick-wave

		API should update Message and MessageTransmission tables with 
		pick-waves and pick-waves response records
		"""
		return


	@vcr.use_cassette('cassettes/group-updates-success-response.yml')
	def testGroupUpdatesSuccessResponse(self):
		"""test FS group-updates API success response for receiving a group-update

		API should return 200 OK response
		"""
		return


	@vcr.use_cassette('cassettes/group-updates-success-database.yml')
	def testGroupUpdatesSuccessDatabase(self):
		"""test FS group-updates API success database update for receiving a group-update

		API should update Message and MessageTransmission tables with 
		group-update and group-update response records
		"""
		return


	def testGroupUpdatesMissingTokenResponse(self):
		"""test FS group-updates API missing token response for receiving a group-update

		API should return an error message
		"""
		return


	def testGroupUpdatesMissingTokenDatabase(self):
		"""test FS group-updates API missing token database update for receiving a group-update

		API should not create Message or MessageTransmission records
		"""
		return


	def testGroupUpdatesIncorrectTokenResponse(self):
		"""test FS group-updates API incorrect token response for receiving a group-update

		API should not create Message or MessageTransmission records
		"""
		return


	def testGroupUpdatesIncorrectTokenDatabase(self):
		"""test FS group-updates API incorrect token database update for receiving a group-update

		API should not create Message or MessageTransmission records
		"""
		return


	@vcr.use_cassette('cassettes/group-cancels-success-response.yml')
	def testGroupCancelsSuccessResponse(self):
		"""test FS group-cancels API success response for receiving a group-cancel

		API should return 200 OK response
		"""
		return


	@vcr.use_cassette('cassettes/group-cancels-success-database.yml')
	def testGroupCancelsSuccessDatabase(self):
		"""test FS group-cancels API success database update for receiving a group-cancel

		API should cancel Message and MessageTransmission tables with 
		group-cancel and group-cancel response records
		"""
		return


	def testGroupCancelsMissingTokenResponse(self):
		"""test FS group-cancels API missing token response for receiving a group-cancel

		API should return an error message
		"""
		return


	def testGroupCancelsMissingTokenDatabase(self):
		"""test FS group-cancels API missing token database update for receiving a group-cancel

		API should not create Message or MessageTransmission records
		"""
		return


	def testGroupCancelsIncorrectTokenResponse(self):
		"""test FS group-cancels API incorrect token response for receiving a group-cancel

		API should not create Message or MessageTransmission records
		"""
		return


	def testGroupCancelsIncorrectTokenDatabase(self):
		"""test FS group-cancels API incorrect token database update for receiving a group-cancel

		API should not create Message or MessageTransmission records
		"""
		return