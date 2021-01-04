from DocumentProcessor import PreprocessorDocument
from QuestionParser import Parser
import time
from Writer import AnswerWriter

if __name__ == "__main__":

    len_sep = 100

    print("#"*len_sep)
    print("Welcome to our Query & Answer System")
    print("-"*len_sep)
    time.sleep(0.5)
    # Path for the films
    padrino = "../documents/padrino.txt"
    psycho = "../documents/psycho.txt"

    print("You can ask questions about El Padrino or Psicosis.")
    print("-"*len_sep)
    time.sleep(0.5)
    # Preprocess films
    padrino = PreprocessorDocument(padrino).preprocess()
    psycho = PreprocessorDocument(psycho).preprocess()

    questions = []

    # Question-Answer loop
    while True:
        question = input("Please, enter a question: ")

        if question == "quit":
            break

        question = Parser(question).parse()
    
        question.answer()

        print("Answer: ", question.get_answer())
        print("-"*len_sep)
        
        questions.append(question)

    print("#"*len_sep)
    
    save = input("Do you want to save your questions and answers? (y/n) : ")
    if save =="y":
        print("writing your answers...")
        writer = AnswerWriter(questions)
        writer.write()
        time.sleep(1)
        print("File correctly written, check /answers folder.")
    elif save == "n":
        print("Okay, you don´t want to save your answers.")
    else:
        print("You introduced a wrong confirmation answer. Good luck next time!")
    
    print("#"*len_sep)
    print("Thanks for using our system!")
    print("#"*len_sep)




