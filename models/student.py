

class Student:
    def __init__(self, student_id, firstname, lastname, email, pwd):
        self.id = student_id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.pwd = pwd
        self.subject = []
        self.average_mark = 0

    def update_average(self):
        if not self.subject:
            self.average_mark = 0
        else:
            total = sum(s.mark for s in self.subject)
            self.average_mark = total / len(self.subject)

    def is_pass(self):
        return self.average_mark >= 50