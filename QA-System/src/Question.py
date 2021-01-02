import re

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

class CriticaQuestion(Question):

    def __init__(self, question, num_rule):
        super().__init__(question)
        self.num_rule = num_rule
        
    def answer(self):
        if self.num_rule == 1: # cuántas críticas
            self.answer = len(self.film["críticas"])
        elif self.num_rule == 2: # cuántos críticos
            criticas = self.film["críticas"]
            autores = [critica["autor"] for critica in criticas]
            self.answer = ", ".join(autores)
        else:
            self.answer = "Error"

class PrizeQuestion(Question):

    def __init__(self, question, num_rule, value = None):
        super().__init__(question)
        self.num_rule = num_rule 
        self.value = value

    def answer(self):
        premios = self.film["premios"]
        if self.num_rule == 1: # cuántos premios
            numeros = 0
            pattern = "^(\d?)\s?([\w+\s]+)"
            for premio in premios:
                institucion = re.match(pattern, premio["institucion"]).groups()[0]
                numeros += int(1) if institucion is "" else int(institucion)
            self.answer = str(numeros) + " premios"

        elif self.num_rule == 2: # qué premios
            self.answer = " - ".join([premio["institucion"] + ": " + premio["categorias"] for premio in premios])
        
        elif self.num_rule == 3:
            self.answer = ", ".join(list(set([premio["año"] for premio in premios])))
        
        elif self.num_rule == 4: # más de
            numeros = 0
            pattern = "^(\d?)\s?([\w+\s]+)"
            for premio in premios:
                institucion = re.match(pattern, premio["institucion"]).groups()[0]
                numeros += int(1) if institucion is "" else int(institucion)
            self.answer = "Sí" if numeros > self.value else "No"
        
        elif self.num_rule == 5: # menos de
            numeros = 0
            pattern = "^(\d?)\s?([\w+\s]+)"
            for premio in premios:
                institucion = re.match(pattern, premio["institucion"]).groups()[0]
                numeros += int(1) if institucion is "" else int(institucion)
            self.answer = "Sí" if numeros < self.value else "No"
        
        elif self.num_rule == 6: # algun
            self.answer = "Sí" if premios is not None else "No"
        
        elif self.num_rule == 7: # algun en
            self.answer = "Sí" if self.value in list(set([premio["año"] for premio in premios])) else "No"

class ValoracionQuestion(Question):

    def __init__(self, question, typeQuest, value = None):
        super().__init__(question)
        self.num_rule = typeQuest
        self.value = value
        
    def answer(self):
        valoracion = self.film["valoracion"]
        if self.num_rule == 1: # qué valoracion
            self.answer = valoracion["puntuación"]
        
        elif self.num_rule == 2: # más de un x
            self.answer = "Sí" if float(valoracion["puntuación"]) > int(self.value) else "No"
        
        elif self.num_rule == 3: # más de un x
            self.answer = "Sí" if float(valoracion["puntuación"]) < int(self.value) else "No"
        
        elif self.num_rule == 4: # cuánta gente valoró
            self.answer = valoracion["votos"]