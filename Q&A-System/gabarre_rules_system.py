# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 14:20:13 2021

@author: Alejandro
"""
from enum import Enum
from typing import Union
import re
#class rule:
    
    
class DimensionNames(str, Enum):
    titulo = "titulo"
    estreno = "estreno"
    duracion = "duracion"
    direccion = "direccion"
    guion = "guion"
    musica = "musica"
    reparto = "reparto"
    productora = "productora"
    genero = "genero"
    grupos = "grupos"
    sinopsis = "sinopsis"
    valoracion = "valoracion"
    votos = "votos"
    premios = "premios"
    criticas = "criticas"
    
    
class ComposedDimensions(str, Enum):
    premios = "premios"
    criticas = "criticas"
    valoracion = "valoracion"
    
class SubDimensionNames(str, Enum):
    anio = "anio"
    institucion = "institucion"
    categoria  = "categoria"
    critica = "critica"
    autores = "autores"

class DocumentBasicDimensions(str, Enum):
    titulo = "TÍTULO ORIGINAL"
    estreno = "AÑO"
    duracion = "DURACIÓN"
    direccion = "DIRECCIÓN"
    guion = "GUIÓN"
    musica = "MÚSICA"
    reparto = "REPARTO"
    productora = "PRODUCTORA"
    genero = "GÉNERO"
    grupos = "GRUPOS"
    sinopsis = "SINOPSIS"
    premios = "PREMIOS"
    criticas = "CRÍTICAS"
    valoracion = "PUNTUACIÓN"
    votos = "VOTOS"

    
    
class Rule:
    def process_rule(self,raw_rule):
        self.process_antecedent(raw_rule)
        self.process_consecuent(raw_rule)

    def process_antecedent(self, raw_rule):
        antecedent_part = raw_rule.split('->')[0]
        clean_rule = antecedent_part.replace(" ","").replace("[","").replace("]","")
        self.rule_elements = clean_rule.split("+")
        for idx, element in enumerate(self.rule_elements):
            if len(element.split('/')) > 1:
                self.rule_elements[idx] = element.split('/')
        
    def process_consecuent(self, raw_rule):
        self.dimension_return_value = raw_rule.split('->')[1].split('[')[-1].split(']')[0]
        
    def execute_rule(self, document: Document):
        for dimension in document.dimensions:
            if dimension.name == self.dimension_return_value:
                return dimension.value

class QuestionProcessor:
    def __init__(self, rules: [Rule], documents: [Document]):
        self.rules = rules
        self.documents = documents
        
    def launch_question(self, question):
        for rule in self.rules:
            matches_count = 0
            for idx, element in enumerate(rule.rule_elements):
                if not isinstance(element, list):
                    if element in question:
                        matches_count += 1
                else:
                    for option in element:
                        option = option.replace("_"," ")
                        if option in question:
                            rule.rule_elements[idx] = option
                            matches_count += 1
                            
            for document in self.documents:
                if document.name in question.lower():
                    question.replace(document.name, 'nombre_pelicula')
                    selectable_document = document
                    matches_count += 1
                    
            print(matches_count)
            print(rule.rule_elements)
            if matches_count == len(rule.rule_elements):
                print(question)
                print(rule.execute_rule(selectable_document))
            
                    
                


class Dimension:
    def __init__(self, name: Union[DimensionNames, SubDimensionNames], value, sub_dimensions: [Dimension] = []):
        self.name = name
        self.value = value
        self.sub_dimensions = sub_dimensions
        

class Document:
    def load_dimensions(self, file_name):
        self.name = file_name.split('/')[-1].split('.')[-2]
        self.dimensions = []
        
        with open(file_name, 'r', encoding="utf8") as document:
            doc_list = [line.replace('\n',"") for line in document if line != '\n']
        idx_list = [i for i, x in enumerate(doc_list) if x.isupper()]
        dim_list = [doc_list[start:end] for start, end in zip([0, *idx_list], [*idx_list, len(doc_list)])]
        del dim_list[0]
        for dim in dim_list:
            document_dimension_name = dim[0]
            value = dim[1:]
            try:
                dimension_name = DocumentBasicDimensions(document_dimension_name).name
            except ValueError as e:
                print(e)
                print(f"Dimensión {dimension_name} no procesada")
                continue
            sub_dimensions = []
            if dimension_name == DimensionNames.premios:
                years = []
                institutions = []
                category = []
                for prize in value:
                    splitted_prize = prize.split(':')
                    years.append(splitted_prize[0].split(" ")[-1])
                    institutions.append(''.join([i for i in splitted_prize[1] if not i.isdigit()]))
                    category.append(splitted_prize[-1])
                dimension_year = Dimension(SubDimensionNames.anio, years)
                dimension_institution = Dimension(SubDimensionNames.institucion, institutions)
                dimension_category = Dimension(SubDimensionNames.categoria, category)
                sub_dimensions = [dimension_year, dimension_institution, dimension_category]
                value = None
                
            elif dimension_name == DimensionNames.criticas:
                critics = []
                authors = []
                for critic in value:
                    author = critic.split('"')[-1]
                    critics.append(critic[:-(len(author)+1)].replace("- \"", ""))
                    authors.append(author)
                dimension_critic = Dimension(SubDimensionNames.critica, critics)
                dimension_author = Dimension(SubDimensionNames.autores, authors)
                sub_dimensions = [dimension_critic, dimension_author]
                value = None
            dimension = Dimension(DimensionNames[dimension_name].value, value, sub_dimensions)
            self.dimensions.append(dimension)
        
    def get_dimensions(self):
        return self.dimensions
            
doc = Document()
doc.load_dimensions(r'./documents/psicosis.txt')
#dimensions = doc.get_dimensions()

rule_str = "Cuándo + [se_estrenó/salió] + nombre_pelicula -> Valor[nombre_pelicula][estreno]"
rule = Rule()
rule.process_rule(rule_str)

question_processor = QuestionProcessor([rule],[doc])
question_processor.launch_question("Cuándo salió la película psicosis")

    
