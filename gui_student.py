import re
import tkinter as tk
from tkinter import messagebox
import random

from models.database import Database
from models.student import Student
from models.subject import Subject

db = Database()
EMAIL_PATTERN = r'^[a-z]+\.[a-z]+@university\.com$'
PASSWORD_PATTERN = r'^[A-Z][a-zA-Z]{5,}\d{3,}$'

class UniversityApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("GUIUniApp")
        self.geometry("500x400")
        self.current_student = None
        self.show_login_window()

    def gen_uniq_student_id(self):
        existing_ids = [s.id for s in db.students]
        while True:
            new_id = f"{random.randint(1, 999999):06}"
            if new_id not in existing_ids:
                return new_id

    def show_login_window(self):
        self.clear_window()
        tk.Label(self, text="Login Window").pack(pady=10)

        tk.Label(self, text="Email").pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack(pady=5)

        tk.Label(self, text="Password").pack()
        #I can add show = "*" for security
        self.pwd_entry = tk.Entry(self, show="*")
        self.pwd_entry.pack(pady=5)
        #padx pady, the number of pixel surrounding the widget
        #pack is they layout manager

        tk.Button(self, text="Login", command=self.login_student).pack(pady=10)
        # tk.Button(self, text="Register", command=self.register_student).pack(pady=10)


    def login_student(self):

        db.load()
        email = self.email_entry.get().lower()
        pwd = self.pwd_entry.get()

        student = db.get_student_by_email(email)
        if not re.match(EMAIL_PATTERN, email):
            messagebox.showerror("Error", "Email must be firstname.lastname@university.com")
            return

        if not re.match(PASSWORD_PATTERN, pwd):
            messagebox.showerror("Invalid Password Format", "Email or Password is Incorrect!")
            return

        if student and student.pwd == pwd:
            self.current_student = student
            self.show_enrolment_window()
        else:
            messagebox.showerror("Login Failed", "Student not found.")

    def show_enrolment_window(self):
        self.clear_window()
        tk.Label(self, text="Enrolment Window", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Add Subject", command=self.add_subject).pack(pady=5)
        tk.Button(self, text="View Subjects", command=self.show_subject_window).pack(pady=5)
        tk.Button(self, text="Logout", command=self.logout).pack(pady=20)

    def add_subject(self):
        if len(self.current_student.subject) >= 4:
            messagebox.showwarning("Limit Exceeded", "Cannot enroll in more than 4 subjects.")
        else:
            subject = Subject()
            self.current_student.subject.append(subject)
            db.save()
            messagebox.showinfo("Success", f"Enrolling in Subject-{subject.id}. \nYou are now enrolled in {len(self.current_student.subject)} out of 4 subjects.")

    def show_subject_window(self):
        self.clear_window()
        tk.Label(self, text="Subject Window", font=("Arial", 16)).pack(pady=10)
        db.students = db.load()
        self.current_student = db.get_student_by_email(self.current_student.email)
        if not self.current_student.subject:
            tk.Label(self, text="No subjects enrolled yet.").pack()
        else:
            for subj in self.current_student.subject:
                info = f"Subject::{subj.id} -- mark: {subj.mark:.2f} -- grade = {subj.grade}"
                tk.Label(self, text=info).pack()

            # Optionally show student's overall average
            self.current_student.update_average()
            tk.Label(self, text=f"\nAverage Mark: {self.current_student.average_mark:.2f}").pack(pady=5)

        tk.Button(self, text="Back", command=self.show_enrolment_window).pack(pady=10)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def logout(self):
        self.current_student = None
        self.show_login_window()

if __name__ == "__main__":
    app = UniversityApp()
    app.mainloop()



# old code
# import tkinter as tk
# from models.database import Database
# from models.student import Student
# from gui_views import EnrolmentFrame, SubjectFrame, LoginFrame, show_subject
#
# EMAIL_PATTERN = r'^[a-z]+\.[a-z]+@university\.com$'
# PASSWORD_PATTERN = r'^[A-Z][a-zA-Z]{5,}\d{3,}$'
# db = Database()
#
# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Student GUI Application")
#         self.geometry("500x500")
#         self.config(bg="#f0f0f0")
#         self.resizable(True,True)
#
#         self.database = db
#         self.current_student = None
#
#         self.show_login()
#     def show_login(self):
#         self.clear_window()
#         LoginFrame(self, self.database)
#
#     def show_enrolment(self, student):
#         self.clear_window()
#         self.current_student = student
#         EnrolmentFrame(self, student, self.database)
#
#     def show_subject(self):
#
#         SubjectFrame(self, self.current_student)
#     def clear_window(self):
#         for widget in self.winfo_children():
#             widget.destroy()
# if __name__ == "__main__":
#     app = App()
#     app.mainloop()
