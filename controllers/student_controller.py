import re
import random
from getpass import getpass
from utils.colors import *
from models.database import Database
from models.student import Student
from models.subject import Subject



#use r'' = for writing regex
# $ = mean end of string
# ^ = start
# [a-z] = any alpha from a to z // the same thing as capital //  [a-zA-Z] = mix with lower and capital
# "\" = to write sth like "."
# \d = num
EMAIL_PATTERN = r'^[a-z]+\.[a-z]+@university\.com$'
PASSWORD_PATTERN = r'^[A-Z][a-zA-Z]{5,}\d{3,}$'
# H + elloo + 123
db = Database()

# =========== Student Menu ==========
def student_menu():
    student_input = input(student("\tStudent System (l/r/x) : ")).lower()
    while (student_input != "x"):
        match student_input:
            #l = login
            case "l":
                login()
            #r = register
            case "r":
                register()
            case _:
                print("\tPlease try again! ")
        student_input = input(student("\tStudent System (l/r/x) : ")).lower()
    print(sys("\tLogging out....."))

def gen_uniq_student_id():
    existing_ids = [s.id for s in db.students]
    while True:
        new_id = f"{random.randint(1, 999999):06}"
        if new_id not in existing_ids:
            return new_id

#new version
def register():
    print(sys("\tStudent Sign Up"))
    while True:
        email = input(student("\tEmail: ")).lower()
        pwd = input(student("\tPassword: "))

        #validate
        if re.match(EMAIL_PATTERN,email) and re.match(PASSWORD_PATTERN, pwd):
            print(succ("\tEmail and Password formats acceptable"))
        else:
            print(error("\tIncorrect email or password format"))
            continue


        try:
            firstname, lastname = email.split("@")[0].split(".")
        except ValueError:
            print(error("\tEmail format must be firstname.lastname@university.com"))
            continue

        if db.get_student_by_email(email):
            print(error(f"\tStudent {firstname.capitalize()} {lastname.capitalize()} already exists."))
            return
        break

    #Name input
    while True:
        name = input(student("\tName: "))
        try:
            firstname,lastname = name.strip().split(" ")
            break
        except ValueError:
            print(error("\tPlease input both firstname and lastname (e.g John Smith)."))
        # print(student(f"\tName: {firstname.capitalize()} {lastname.capitalize()}"))
    student_id = gen_uniq_student_id()

    print(succ(f"\tEnrolling Student {firstname.capitalize()} {lastname.capitalize()}"))
    new_student = Student(student_id, firstname, lastname, email, pwd)
    db.add_student(new_student)
    return

# old version
# def register():
#     print(sys("\tStudent Sign Up"))
#     #name + email
#     while True:
#         firstname = input(student("\tWhat is your first name? ")).lower()
#         lastname = input(student("\tWhat is your last name? ")).lower()
#         email = f"{firstname}.{lastname}@university.com"
#         if db.get_student_by_email(email):
#             print(error("\tEmail is already exists. Please try again with different name"))
#             continue
#         #validate email
#         if re.match(EMAIL_PATTERN, email):
#             break
#         else:
#             print(error("\tInvalid email generated. Use only letters for name (no space or numbers)"))
#     # print(succ(f"Your student email is: {firstname}.{lastname}@university.com"))
#
#     #Password
#     while True:
#         # pwd = getpass(student("New password (Hidden): "))
#         pwd = input(student("\tNew password: "))
#         if re.match(PASSWORD_PATTERN, pwd):
#             break
#         else:
#             print(error("\tInvalid password format. Password must start with uppercase, have at least 5 letters and 3 digits."))
#     # ID
#     student_id = gen_uniq_student_id()
#
#
#     print(succ(f"\tEnrolling Student {firstname} {lastname}"))
#     # print(succ("\nRegistration completed!"))
#     # print(succ(f"Student ID: {student_id}"))
#     # print(succ(f"Student Name: {firstname} {lastname}"))
#     # print(succ(f"Student Email: {email}"))
#     # print(succ(f"{pwd} Password is set and saved securely!"))
#
#     new_student = Student(student_id, firstname, lastname, email,pwd)
#     db.add_student(new_student)
#     return

def login():
    print(sys("\tStudent Sign In"))
    while True:
        try:

            email = input(student("\tEnter your student email: "))
            if email == 'x':
                print(sys("\tCancelled login. Returning to student Menu..."))
                return
            pwd = input(student("\tEnter your password: ")) #getpasss

            if not re.match(EMAIL_PATTERN, email):
                print(error("\tInvalid email or password format."))
                continue

            student_obj = db.get_student_by_email(email) #Check email in DB

            if student_obj is None or student_obj.pwd != pwd:
                print(error("\tIncorrect email or password format. "))
                continue

            print(succ("\tEmail and Password formats Acceptable! "))
            # print(succ(f"\nWelcome {student_obj.firstname.capitalize()} {student_obj.lastname.capitalize()}!"))
            # print(succ("You have successfully logged in! "))
            student_function(student_obj)
            return
        except ValueError as ve:
            print(error(str(ve)))
        except Exception as e:
            print(error("\tSomething went wrong during login, Please try again! "))


# =========== Student Function ==========
def student_function(student_obj):
    print(sys("\t\t===== Student Menu ====="))
    student_input = input(student("\t\tStudent Course Menu (c/e/r/s/x): ")).lower()
    while (student_input != "x"):
        db.students = db.load()  # refresh in-memory list
        student_obj = db.get_student_by_email(student_obj.email)  # refresh object
        match student_input:
            case "c":
                change_pwd(student_obj)
            case "e":
                subject_enrol(student_obj)
            case "r":
                sub_remove(student_obj)
            case "s":
                show_sub(student_obj)
            case _:
                print(student("\t\tPlease try again: "))
        student_input = input(student("\t\tStudent Course Menu (c/e/r/s/x): ")).lower()

    print(sys("\t\tLogging out from Student Menu..."))

def subject_enrol(student_obj):
    if len(student_obj.subject) >= 4:
        print(error("\t\tStudents are allowed to enrol in 4 subjects only! "))
        return

    new_subject = Subject()
    student_obj.subject.append(new_subject)
    student_obj.update_average()
    db.save()

    print(sys(f"\t\tEnrolling in Subject-{new_subject.id}"))
    print(sys(f"\t\tYou are now enrolled in {len(student_obj.subject)} out of 4 subjects"))

def show_sub(student_obj):
    # print(sys("===== Your Enrolled Subject ======"))
    if not student_obj.subject:
        print(error("\t\tShowing 0 subjects"))
    else:
        print(sys(f"\t\tShow {len(student_obj.subject)} subjects"))
        for s in student_obj.subject:
            print(sys(f"\t\t[ Subject::{s.id} -- mark = {s.mark} -- grade = {s.grade:<2} ]")) # <2 mean align the letter

def sub_remove(student_obj):
    print(sys("\t\t===== Remove Subject ======"))
    if not student_obj.subject:
        print(error("\t\tYou have no subjects to remove"))

    # print(succ(f"Show {len(student_obj.subject)} subjects"))
    for s in student_obj.subject:
        print(sys(f"\t\t[ Subject::{s.id} -- mark = {s.mark} -- grade = {s.grade} ]"))

    subject_id = input(student("\t\tRemove Subject by ID: "))
    subject_to_remove = None
    for s in student_obj.subject:
        if s.id == subject_id:
            subject_to_remove = s

    if subject_to_remove:
        student_obj.subject.remove(subject_to_remove)
        student_obj.update_average()
        db.save()
        print(sys(f"\t\tDropping Subject - {subject_to_remove.id}"))
        print(sys(f"\t\tYou are now enrolled in {len(student_obj.subject)} out of 4 subjects"))
    else:
        print(error("\t\tSubject ID not found. Please check and try again! "))

def change_pwd(student_obj):
    print(sys("\t\tUpdating Password"))
    while True:
        new_pwd = input(student("\t\tEnter new password: "))
        confirm_pwd = input(student("\t\tConfirm Password: "))
        if new_pwd == confirm_pwd:
            if re.match(PASSWORD_PATTERN, new_pwd):
                student_obj.pwd = new_pwd
                db.save()
                print(succ("\t\tPassword changed successfully! "))
                break
            else:
                print(error("\t\tInvalid password format. Password must start with uppercase, have at least 5 letters and 3 digits."))
        else:
            print(error("\t\tPassword does not match - Try again! "))

