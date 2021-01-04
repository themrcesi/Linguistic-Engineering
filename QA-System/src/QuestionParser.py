from DocumentProcessor import PreprocessorDocument
from Question import *
import re

year_regex = 'en (el año)? \d{4}$'

before_year_regex = 'antes de (el año)? \d{4}$'
after_year_regex = '(después|despues) de (el año)? \d{4}$'

duration_regex = '[0-9]+'

direction_regex = '(dirigio|dirigió) (\w+)'

screenwritter_regex = '(\w+) el guionista'

category_regex = '(genero|género) (\w+)'

actor_regex = '(participó|participo|actuó|actuo) (\w+)'

saga_regex = 'saga ([^.]+|\S+)'
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
        if ("cuál" in q or "cual" in q) and "original" in q and ("nombre" in q or "título" in q or "titulo" in q):
            quest = TitleQuestion(q)
        # ESTRENO
        elif ("cuándo" in q or "cuando" in q) and ("se estrenó" in q or "se estreno" in q or "salió" in q or "salio" in q):
            quest = PremiereQuestion(q,0)
            
        elif ("se estrenó" in q or "se estreno" in q or "salió" in q or "salio" in q) \
                and re.findall(year_regex, q) != []:
            quest = PremiereQuestion(q,1, re.findall(year_regex, q)[0].split(' ')[-1])
            
        elif ("se estrenó" in q or "se estreno" in q or "salió" in q or "salio" in q) \
                and re.findall(before_year_regex, q) != []:
            quest = PremiereQuestion(q, 2, re.findall(before_year_regex, q)[0].split(' ')[-1])
            
        elif ("se estrenó" in q or "se estreno" in q or "salió" in q or "salio" in q) \
                and re.findall(after_year_regex, q) != []:
            quest = PremiereQuestion(q, 3, re.findall(after_year_regex, q)[0][1].split(' ')[-1])
            
        # DURACIÓN
        
        elif ("cuánto" in q or "cuanto" in q) and "dura" in q:
            quest = DurationQuestion(q, 0)
            
        elif "dura" in q and ("más de" in q or "mas de" in q) and re.findall(duration_regex,q) != [] and "minutos" in q:
            quest = DurationQuestion(q, 1, re.findall(duration_regex,q)[0])
            
        elif "dura" in q and ("más de" in q or "menos de" in q) and re.findall(duration_regex,q) != [] and "minutos" in q:
            quest = DurationQuestion(q, 2, re.findall(duration_regex,q)[0])

        # DIRECCIÓN
        elif ("quién" in q or "quien" in q) and ("dirig" in q or "director" in q):
            quest = DirectionQuestion(q, 0)
            
        elif re.findall(direction_regex,q) != []:
            quest = DirectionQuestion(q, 1, re.findall(direction_regex,q)[0][1])
        # GUIÓN
        elif ("quién" in q or "quien" in q) and "guionista" in q:
            quest = ScreenwritterQuestion(q, 0)
            
        elif ("fue" in q or "es" in q or "ha sido" in q) and re.findall(screenwritter_regex,q) != []: #Pendiente
            quest = ScreenwritterQuestion(q, 1, re.findall(screenwritter_regex,q)[0])
            
        elif ("cuántos" in q or "cuantos" in q) and "guionista" in q:
            quest = ScreenwritterQuestion(q, 2)

        # MÚSICA
        elif ("quién" in q or "quien" in q) and "compuso" in q and "banda sonora" in q:
            quest = MusicQuestion(q)

        # REPARTO
        elif ("qué" in q or "que" in q) and ("actor" in q or "actri" in q) and \
            ("tiene" in q or "particip" in q or "actua" in q):
            quest = CastQuestion(q, 0)
        
        elif ("quienes" in q or "quiénes" in q) and re.findall(duration_regex,q) != [] and "actores principales" in q:
            num_actors = int(re.findall(duration_regex,q)[0])
            quest = CastQuestion(q, 1, principal_actors = num_actors)

        elif re.findall(actor_regex,q) != []:
            actor = re.findall(actor_regex,q)[0][1]
            quest = CastQuestion(q, 2, actor = actor)
            
        # PRODUCTORA
        elif ("cuál" in q or "cual" in q) and "productora" in q:
            quest = ProducerQuestion(q)
        # GÉNERO
        elif ("qué" in q or "que" in q) and ("genero" in q or "género" in q or "categoría" in q or "categoria" in q):
            quest = GenderQuestion(q, 0)
            
        elif ("fue" in q or "es" in q or "ha sido" in q) and re.findall(category_regex,q) != []:
            gender = re.findall(category_regex,q)[0][1].split(' ')[-1]
            quest = GenderQuestion(q, 1, gender)

        # GRUPOS
        elif ("qué" in q or "que" in q) and "saga" in q:
            quest = GroupQuestion(q, 0)
        elif ("pertenece" in q or "es" in q) and re.findall(saga_regex,q) != []:
            saga = re.findall(saga_regex,q)[0]
            quest = GroupQuestion(q, 1, saga)

        # SINOPSIS
        elif ("cuál" in q or "cual" in q) and ("resumen" in q or "sinopsis" in q):
            quest = SynopsisQuestion(q)
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
        elif re.findall("((en (qué|que) años)|(cuando|cuándo)).+premios",q):#(("cuando" in q or "cuándo" in q) or ("en qué años" in q or "en que años") and "premios" in q):
            quest = PrizeQuestion(q, 3)
        elif re.findall("(que|qué).premios", q): #("qué" in q or "que" in q) and "premios" in q: # qué premios MIRAR
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
        else:
            return IncorrectQuestion(q)

        return quest

