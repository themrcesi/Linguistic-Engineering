import os
import time

class AnswerWriter():

    def __init__(self, questions):
        self.questions = questions
        
    def write(self):
        path = "../answers/" + time.strftime("%Y%m%d-%H%M%S") + "_answers.txt"
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "a+", encoding = "utf-8") as f:
            for question in self.questions:
                f.write(question.__str__() + "\n")
