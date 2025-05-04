import os
import pickle

class Database:
    def __init__(self, filepath = './students.data'):
        self.filepath = filepath
        self.students = self.load() #load data

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath,'rb') as f:
                return pickle.load(f)
        return []

    def save(self):
        with open(self.filepath, 'wb') as f:
            pickle.dump(self.students, f)

    def add_student(self, student):
        self.students.append(student)
        self.save()

    def get_student_by_email(self, email):
        return next((s for s in self.students if s.email == email), None)

    def clear(self):
        self.students=[]
        self.save()