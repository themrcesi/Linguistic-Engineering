import re
import unicodedata
import glob
import pathlib
import random

from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from joblib import Parallel, delayed



REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)|(\⁰)|(\•)|(\\')")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
NO_SPACE = ""
SPACE = " "
STOP_WORDS = set(stopwords.words('english'))

def remove_accents(token):
    try:
        token = unicode(token, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    token = unicodedata.normalize('NFD', token)
    token = token.encode('ascii', 'ignore')
    token = token.decode("utf-8")
    return str(token)
    
def delete_stop_words(doc):
    tokens = wordpunct_tokenize(doc)
    clean = [remove_accents(token) for token in tokens if token.lower() not in STOP_WORDS and len(token) > 2]
    return clean

def preprocess_document(document_path):
    print("Document path: ",document_path)
    with open(document_path, "r",encoding="utf8") as f:
        document = f.read()
    document = remove_accents(document.lower())
    document = REPLACE_NO_SPACE.sub(NO_SPACE, document)
    document = REPLACE_WITH_SPACE.sub(SPACE, document)
    document = delete_stop_words(document)
    return document
    

def get_clean_docs(folder_path):
    documents_paths = glob.glob(folder_path)
    documents_paths = random.choices(documents_paths, k=15)
    processed_docs = Parallel(n_jobs=16)(delayed(preprocess_document)(path) for path in documents_paths)
    return processed_docs

current_path = pathlib.Path().absolute()
health_folder_path = str(current_path)+"\documents\health\*"
politics_folder_path = str(current_path)+"\documents\politics\*"
sports_folder_path = str(current_path)+"\documents\sports\*"

health_docs = get_clean_docs(health_folder_path)
politics_docs = get_clean_docs(politics_folder_path)
sports_docs = get_clean_docs(sports_folder_path)