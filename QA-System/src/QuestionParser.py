from DocumentProcessor import PreprocessorDocument
from Question import *
import re

class Parser():

    # Path for the films
    padrino = "../documents/padrino.txt"
    psycho = "../documents/psycho.txt"

    # Preprocess films
    padrino = PreprocessorDocument(padrino).preprocess()
    psycho = PreprocessorDocument(psycho).preprocess()

    def __init__(self, question):
        self.question = question

    def parse(self):
        q = self.question.lower()

        # TÍTULO
        if ("cuál" in q or "cual" in q) and "original" in q and ("nombre" in q or "título" in q):
            quest = TitleQuestion(q)
        # ESTRENO

        # DURACIÓN

        # DIRECCIÓN

        # GUIÓN

        # MÚSICA

        # REPARTO

        # PRODUCTORA

        # GÉNERO

        # GRUPOS

        # SINOPSIS

        # VALORACIÓN
        elif ("que" in q or "qué" in q) and ("valoración" in q or "valoracion" in q or "puntuación" in q or "puntuacion" in q):
            quest = ValoracionQuestion(q, 1)
        elif re.findall("tiene (más|mas) (valoración |puntuación |valoracion |puntuacion )?de un (\d+)", q):
            value = re.findall("tiene (mas|más) (valoración |puntuación |valoracion |puntuacion )?de un (\d+)", q)[0][2]
            quest = ValoracionQuestion(q, 2, value)
            print(value)
        elif re.findall("tiene menos (valoración |puntuación |valoracion |puntuacion )?de un (\d+)", q):
            value = re.findall("tiene menos (valoración |puntuación |valoracion |puntuacion )?de un (\d+)", q)[0][1]
            quest = ValoracionQuestion(q, 3, value)
        elif ((("cuánta" in q or "cuanta" in q) and "gente" in q) or (("cuántas" in q or "cuantas" in q) and "personas" in q)) and ("puntu" in q or "valor" in q):
            quest = ValoracionQuestion(q, 4)

        # PREMIOS
        elif re.findall("(mas|más) de\s(\d+) premios", q): # ganado mas de x premios
            value = int(re.findall("(mas|más) de\s(\d+) premios", q)[0][1])
            quest = PrizeQuestion(q, 4, value)
        elif re.findall("menos de\s(\d+) premios", q): # ganado menos de x premios
            value = int(re.findall("menos de\s(\d+) premios", q)[0])
            quest = PrizeQuestion(q, 5, value)
        elif ("cuántos" in q or "cuantos" in q) and "premios" in q: # cuántos premios
            quest = PrizeQuestion(q, 1)
        elif ("cuando" in q or "cuándo" in q or "en qué años" in q or "en que años") and "premios" in q:
            quest = PrizeQuestion(q, 3)
        elif ("qué" in q or "que" in q) and "premios" in q: # qué premios MIRAR
            quest = PrizeQuestion(q, 2)
        elif ("gan" in q or "recib" in q) and ("algún premio" in q or "algun premio" in q):
            if re.findall("en (\d{4})", q): # ganado algún en x año
                year = re.findall("en (\d{4})", q)[0]
                quest = PrizeQuestion(q, 7, year)
            else: # ganado algún
                quest = PrizeQuestion(q, 6)     

        # CRÍTICAS
        elif ("cuántas" in q or "cuantas" in q) and ("reseñas" in q or "críticas" in q or "criticas" in q): # cuántos críticas
            quest = CriticaQuestion(q, 1)
        elif ("quienes" in q or "quiénes" in q) and (("autores" in q and ("críticas" in q or "criticas" in q)) or "críticos" in q or "criticos" in q): # quiénes críticos
            quest = CriticaQuestion(q, 2)

        # OTRA
        else:
            quest = UnknownQuestion(q)

        # Check film
        if "el padrino" in q or "padrino" in q:
            quest.set_film(self.padrino)
        elif "psicosis" in q:
            quest.set_film(self.psycho)

        return quest

