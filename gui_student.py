import tkinter as tk
from models.database import Database
from models.student import Student
from gui_views import EnrolmentFrame, SubjectFrame, LoginFrame

EMAIL_PATTERN = r'^[a-z]+\.[a-z]+@university\.com$'
PASSWORD_PATTERN = r'^[A-Z][a-zA-Z]{5,}\d{3,}$'
db = Database()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student GUI Application")
        self.geometry("500x500")
        self.config(bg="#f0f0f0")
        self.resizable(True,True)

        self.database = db
        self.current_student = None

        self.show_login()
    def show_login(self):
        self.clear_window()
        LoginFrame(self, self.database)

    def show_enrolment(self, student):
        self.clear_window()
        self.current_student = student
        EnrolmentFrame(self, student, self.database)

    def show_subject(self):

        SubjectFrame(self, self.current_student)
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
if __name__ == "__main__":
    app = App()
    app.mainloop()
