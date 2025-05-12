import random
import tkinter as tk
from tkinter import messagebox
import re
from models.database import Database
from models.student import Student
from models.subject import Subject



EMAIL_PATTERN = r'^[a-z]+\.[a-z]+@university\.com$'
PASSWORD_PATTERN = r'^[A-Z][a-zA-Z]{5,}\d{3,}$'
db = Database()

class LoginFrame(tk.LabelFrame):
    def __init__(self, master, database):
        super().__init__(master, text="Login", padx=20, pady=20)
        self.master =master
        self.database = database
        self.pack(pady=50)

        tk.Label(self, text= "Email: ").grid(row=0, column=0, sticky="w")
        self.email_entry=tk.Entry(self)
        self.email_entry.grid(row=0, column=1)

        tk.Label(self, text="Password: ").grid(row=1, column=0, sticky="w")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Button(self, text="Login", command=self.login).grid(row=2, columnspan=2, pady=10)
        tk.Button(self, text="Register", command=self.register).grid(row=2, columnspan=1, pady=10)

    def login(self):
        email = self.email_entry.get().lower()
        pwd = self.password_entry.get()

        if not re.match(EMAIL_PATTERN, email):
            messagebox.showerror("Error", "Invalid email format.")
            return
        student = self.database.get_student_by_email(email)

        if student is None or student.pwd != pwd:
            messagebox.showerror("Error", "Incorrect email or password.")
            return

        self.master.show_enrolment(student)

    def register(self):
        reg = tk.Toplevel()
        reg.title("Register")
        reg.geometry("300x300")

        tk.Label(reg, text="First Name: ").pack()
        fname_entry = tk.Entry(reg)
        fname_entry.pack()

        tk.Label(reg, text ="Lastname: ").pack()
        lname_entry = tk.Entry(reg)
        lname_entry.pack()

        tk.Label(reg, text="Password: ").pack()
        pwd_entry= tk.Entry(reg, show="*")
        pwd_entry.pack()

        def create_acc():
            firstname = fname_entry.get().lower()
            lastname = lname_entry.get().lower()
            pwd=pwd_entry.get()

            email = f"{firstname}.{lastname}@university.com"
            if not firstname or not lastname:
                messagebox.showerror("Error", "First name and last name cannot be empty. ")
                return

            if not re.match(PASSWORD_PATTERN, pwd):
                messagebox.showerror("Error", "Invalid Password format.")
                return

            if self.database.get_student_by_email(email):
                messagebox.showerror("Error", "Email already exists.")
                return

            student_id = f"{random.randint(1,999999):06}"
            new_student = Student(student_id, firstname, lastname, email, pwd)
            self.database.add_student(new_student)

            messagebox.showinfo("Success", f"Account created: Email :{email}, Student ID: {student_id}")
            reg.destroy()
        tk.Button(reg, text="Create Account", command=create_acc).pack(pady=10)

class EnrolmentFrame(tk.LabelFrame):
    def __init__(self, master, student, database):
        super().__init__(master, text="Enrolment", padx=20, pady=20)
        self.master = master
        self.student = student
        self.database = database
        self.pack(pady=50)

        tk.Label(self, text=f"Welcome {student.firstname.capitalize()} {student.lastname.capitalize()}").pack()

        self.sub_label = tk.Label(self, text=f"Enrolled subjects: {len(student.subject)} out of 4 subjects")
        self.sub_label.pack()

        self.listbox = tk.Listbox(self, width=50)
        self.listbox.pack()

        for s in student.subject:
            self.listbox.insert(tk.END, f"Subject:: {s.id} -- mark = {s.mark} -- grade = {s.grade}")

        tk.Button(self, text="Enrol in subject", command=self.enrol_subject).pack(pady=5)
        tk.Button(self, text="View Subjects", command= self.view_subject).pack(pady=5)

    def enrol_subject(self):
        if len(self.student.subject)>=4:
            messagebox.showerror("Error", "Cannot enrol more than 4 subjects")
            return

        new_subject = Subject()
        self.student.subject.append(new_subject)
        self.student.update_average()
        self.database.save()

        self.listbox.insert(tk.END, f"Subject:: {new_subject.id} -- mark = {new_subject.mark}  -- grade = {new_subject.grade}")
        self.sub_label.config(text=f"Enrolled Subjects: {len(self.student.subject)} out of 4 subjects")

    def view_subject(self):
        self.master.show_subject()

class SubjectFrame(tk.LabelFrame):
    def __init__(self, master, student):
        super().__init__(master, text="Subject", padx= 20, pady=20)
        self.master = master
        self.student = student
        self.pack(pady=50)

        if not student.subject:
            tk.Label(self, text="No enrolled subjects.").pack()
        else:
            for s in student.subject:
                tk.Label(self, text=f"Subject::{s.id} -- mark: {s.mark} -- grade: {s.grade}").pack()

        tk.Button(self, text="Back to Enrolment", command= lambda: self.back_to_enrolment).pack(pady=10)

    def back_to_enrolment(self):
        self.master.show_enrolment(self.student)