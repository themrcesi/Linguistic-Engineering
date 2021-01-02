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
        
class PremiereQuestion(Question):
    def __init__(self, question, num_rule, numeric_year = None):
        super().__init__(question)
        self.num_rule = num_rule
        self.numeric_year = numeric_year
    
    def answer(self):
        if self.num_rule == 0:
            self.answer = self.film["año"]
        elif self.num_rule == 1:
            self.answer = "Si" if self.film["año"] == self.numeric_year else "No"
        elif self.num_rule == 2:
            self.answer = "Si" if int(self.film["año"]) < int(self.numeric_year) else "No"
        elif self.num_rule == 3:
            self.answer = "Si" if int(self.film["año"]) > int(self.numeric_year) else "No"
            
class DurationQuestion(Question):
    def __init__(self, question, num_rule, minutes = None):
        super().__init__(question)
        self.num_rule = num_rule
        self.minutes = minutes
    
    def answer(self):
        if self.num_rule == 0:
            self.answer = self.film["duración"]
        elif self.num_rule == 1:
            self.answer = "Si" if int(self.film["duración"].split(' ')[0]) > int(self.minutes) else "No"
        elif self.num_rule == 2:
            self.answer = "Si" if int(self.film["duración"].split(' ')[0]) < int(self.minutes) else "No"
            
class DirectionQuestion(Question):
    def __init__(self, question, num_rule, director = None):
        super().__init__(question)
        self.num_rule = num_rule
        self.director = director
    
    def answer(self):
        if self.num_rule == 0:
            self.answer = self.film["dirección"]
        elif self.num_rule == 1:
            self.answer = "Si" if self.director in self.film["dirección"].lower() else "No"
            
class ScreenwritterQuestion(Question):
    def __init__(self, question, num_rule, screenwritter = None):
        super().__init__(question)
        self.num_rule = num_rule
        self.screenwritter = screenwritter
    
    def answer(self):
        if self.num_rule == 0:
            self.answer = self.film["guión"]
        elif self.num_rule == 1:
            self.answer = "Si" if self.screenwritter in self.film["guión"].lower() else "No"
        elif self.num_rule == 2:
            self.answer = len(self.film["guión"].split(','))
            
class MusicQuestion(Question):

    def answer(self):
        self.answer = self.film["música"]
        
class CastQuestion(Question):
    def __init__(self, question, num_rule, principal_actors = 3, actor = None):
        super().__init__(question)
        self.num_rule = num_rule
        self.actor = actor
        self.principal_actors = principal_actors
    
    def answer(self):
        if self.num_rule == 0:
            self.answer = self.film["reparto"]
        elif self.num_rule == 1:
            all_actors = self.film["reparto"].split(',')
            if len(all_actors) < self.principal_actors:
                self.principal_actors = len(all_actors)
            self.answer = ','.join(all_actors[:self.principal_actors])
        elif self.num_rule == 2:
            self.answer = "Si" if self.actor in self.film["reparto"].lower() else "No"
            
class ProducerQuestion(Question):

    def answer(self):
        self.answer = self.film["productora"]
        
class GenderQuestion(Question):
    def __init__(self, question, num_rule, gender = None):
        super().__init__(question)
        self.num_rule = num_rule
        self.gender = gender
    
    def answer(self):
        if self.num_rule == 0:
            self.answer = self.film["género"]
        elif self.num_rule == 1:
            self.answer = "Si" if self.gender in self.film["género"].lower() else "No"
            
class GroupQuestion(Question):
    def __init__(self, question, num_rule, saga = None):
        super().__init__(question)
        self.num_rule = num_rule
        self.saga = saga
    
    def answer(self):
        if self.num_rule == 0:
            self.answer = self.film["grupos"]
        elif self.num_rule == 1:
            self.answer = "Si" if self.saga in self.film["grupos"].lower() else "No"
            
class SynopsisQuestion(Question):

    def answer(self):
        self.answer = self.film["sinopsis"]

class UnknownQuestion(Question):

    def answer(self):
        self.answer = "We don´t have an answer for you question."
