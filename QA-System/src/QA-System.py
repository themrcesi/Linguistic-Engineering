from DocumentProcessor import PreprocessorDocument

if __name__ == "__main__":

    padrino = "../documents/padrino.txt"
    psycho = "../documents/psycho.txt"

    padrino = PreprocessorDocument(padrino).preprocess()
    psycho = PreprocessorDocument(psycho).preprocess()