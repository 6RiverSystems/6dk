from random import choice


class DkProfile():
	def __init__(self, standard_profile, adjectives, nouns):
		self.standard_profile = standard_profile
		self.adjectives = adjectives
		self.nouns = nouns


	def make_profile(self):
		profile = self.standard_profile
		profile['friendly_name'] = 	'-'.join([choice(self.adjectives).lower(), 
												choice(self.nouns).lower(),
												str(choice(range(1000,9999)))])
		return profile