from DocumentProcessor import PreprocessorDocument
from Question import TitleQuestion, UnknownQuestion

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

        # PREMIOS

        # CRÍTICAS

        # OTRA
        else:
            quest = UnknownQuestion(q)

        # Check film
        if "el padrino" in q or "padrino" in q:
            quest.set_film(self.padrino)
        elif "psicosis" in q:
            quest.set_film(self.psycho)

        return quest

