class Question():

    def __init__(self, question):
        self.question = question

    def set_film(self, film):
        self.film = film
    
    def answer(self):
        pass

    def get_answer(self):
        return self.answer

    def __str__(self):
        return "- Question = " + self.question + "\t Answer: " + self.answer

class TitleQuestion(Question):

    def answer(self):
        self.answer = self.film["título original"]

class UnknownQuestion(Question):

    def answer(self):
        self.answer = "We don´t have an answer for you question."
