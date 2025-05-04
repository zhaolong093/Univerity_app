import random

class Subject:
    def __init__(self):
        self.id = f"{random.randint(1,999):03}"
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