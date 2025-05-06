import random

class Subject:
    def __init__(self, id = None):
        self.id = id if id else f"{random.randint(1,999):03}" #check unique ID
        self.mark = random.randint(25,100)
        self.grade = self.get_grade()

    def get_grade(self):
        if self.mark >= 85:
            return "HD"
        elif self.mark >= 75:
            return "D"
        elif self.mark >=65:
            return "C"
        elif self.mark >= 50:
            return "P"
        else:
            return "F"