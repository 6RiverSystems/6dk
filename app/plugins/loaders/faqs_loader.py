

class DkFaqs():

    def __init__(self):
        self.faqs = []

    def update(self, faqs):
        self.faqs = faqs

    def get(self):
        return self.faqs
