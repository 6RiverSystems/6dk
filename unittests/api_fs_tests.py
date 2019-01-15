import vcr

from unittests.base import sixDKTests


class ApiFsTests(sixDKTests):

	"""
	@vcr.use_cassette('cassettes/pick-waves-success-response.yml')
	def testPickWavesSuccessResponse(self):
		""test FS API success response for receiving a pick-wave

		API should return 200 OK response
		""
		user, profile = self.create_user(include_profile=True)
		response = self.app.post('/dev/wis-southbound/2.3/pick-waves',
								data=self.get_payload('sdk-pick-wave.json'),
								headers={'6Dk-Token': profile['token_id']})
		self.assertEqual(response.status_code, 200)		
		return
	"""


	@vcr.use_cassette('cassettes/pick-waves-success-database.yml')
	def testPickWavesSuccessDatabase(self):
		return


	def testPickWavesMissingToken(self):
		return


	def testPickWavesIncorrectToken(self):
		return


	def testExceptionPickWavesSuccessResponse(self):
		return


	def testExceptionPickWavesSuccessDatabase(self):
		return


	def testExceptionPickWavesMissingToken(self):
		return


	def testExceptionPickWavesIncorrectToken(self):
		return


	def testGroupUpdatesSuccessResponse(self):
		return


	def testGroupUpdatesSuccessDatabase(self):
		return


	def testGroupUpdatesMissingToken(self):
		return


	def testGroupUpdatesIncorrectToken(self):
		return


	def testGroupCancelsSuccessResponse(self):
		return


	def testGroupCancelsSuccessDatabase(self):
		return


	def testGroupCancelsMissingToken(self):
		return


	def testGroupCancelsIncorrectToken(self):
		return