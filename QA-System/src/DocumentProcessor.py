import numpy as np
import re

class Data():

    def __init__(self, name):
        self.key = name

    def get_key(self):
        return self.key

    def _set_value(self, value):
        self.value = value

    def get_dic(self):
        return {self.key.lower(): self.value}

    def get_value(self, document):
        index_key = document.index(self.key)
        self._set_value(document[index_key + 1])
        return self


class ValoracionData(Data):

    def get_dic(self):
        return {"valoracion": {self.key[0].lower(): self.value[0], self.key[1].lower(): self.value[1]}}

    def get_value(self, document):
        index_key_puntuacion = document.index(self.key[0])
        index_key_votos = document.index(self.key[1])
        self._set_value(
            (document[index_key_puntuacion + 1], document[index_key_votos + 1]))
        return self


class PremiosData(Data):

    def get_dic(self):
        return {self.key[0].lower(): self.value}

    def get_value(self, document):
        index_key = document.index(self.key[0])
        next_index_key = document.index(self.key[1])
        values = document[index_key + 1:next_index_key-1]
        values = [self._preprocess_premio(value) for value in values]
        self._set_value(values)
        return self

    def _preprocess_premio(self, premio):
        values = premio.split(":")
        año = values[0].split(" ")[1]
        institucion = values[1].strip()
        categorias = values[2]
        return {"año": año, "institucion": institucion, "categorias": categorias}


class CriticasData(Data):

    def get_value(self, document):
        index_key = document.index(self.key)
        values = document[index_key + 1:]
        values = [self._preprocess_critica(value) for value in values]
        self._set_value(values)
        return self

    def _preprocess_critica(self, critica):
        match = re.search("(\".+\") (.+)", critica)
        critica = match.group(1).replace("\"", "")
        autor = match.group(2)
        return {"critica": critica, "autor": autor}


class PreprocessorDocument():

    HEADING_TITULO = "TÍTULO ORIGINAL"
    HEADING_AÑO = "AÑO"
    HEADING_DURACION = "DURACIÓN"
    HEADING_PAIS = "PAÍS"
    HEADING_DIRECCION = "DIRECCIÓN"
    HEADING_GUION = "GUIÓN"
    HEADING_MUSICA = "MÚSICA"
    HEADING_FOTOGRAFIA = "FOTOGRAFÍA"
    HEADING_REPARTO = "REPARTO"
    HEADING_PRODUCTORA = "PRODUCTORA"
    HEADING_GENERO = "GÉNERO"
    HEADING_GRUPOS = "GRUPOS"
    HEADING_SINOPSIS = "SINOPSIS"
    HEADING_PUNTUACION = "PUNTUACIÓN"
    HEADING_VOTOS = "VOTOS"
    HEADING_PREMIOS = "PREMIOS"
    HEADING_CRITICAS = "CRÍTICAS"

    def __init__(self, document):
        lines = [line.strip() for line in open(
            document, encoding="utf-8").readlines()]
        self.document = lines

    def preprocess(self):
        info = {}
        simple = [self.HEADING_TITULO, self.HEADING_AÑO, self.HEADING_DURACION, self.HEADING_PAIS, self.HEADING_DIRECCION, self.HEADING_GUION, self.HEADING_MUSICA,
                  self.HEADING_FOTOGRAFIA, self.HEADING_REPARTO, self.HEADING_PRODUCTORA, self.HEADING_GENERO, self.HEADING_GRUPOS, self.HEADING_SINOPSIS]
        for heading in simple:
            info = dict(
                info, **Data(heading).get_value(self.document).get_dic())
        info = dict(info, **ValoracionData([self.HEADING_PUNTUACION,
                                            self.HEADING_VOTOS]).get_value(self.document).get_dic())
        info = dict(
            info, **PremiosData([self.HEADING_PREMIOS, self.HEADING_CRITICAS]).get_value(self.document).get_dic())
        info = dict(
            info, **CriticasData(self.HEADING_CRITICAS).get_value(self.document).get_dic())
        return info