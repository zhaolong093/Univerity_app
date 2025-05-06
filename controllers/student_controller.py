import re
import random
from getpass import getpass
from utils.colors import *
from models.database import Database
from models.student import Student
from models.subject import Subject



#use r'' = for writing regex
# $ = mean end of string
EMAIL_PATTERN = r'^[a-z]+\.[a-z]+@university\.com$'
PASSWORD_PATTERN = r'^[A-Z][a-zA-Z]{5,}\d{3,}$'
db = Database()




# =========== Student Menu ==========
def student_menu():
    student_input = input(student("Student System (l/r/x) : ")).lower()
    while (student_input != "x"):
        match student_input:
            #l = login
            case "l":
                login()
            #r = register
            case "r":
                register()
            case _:
                print("Please try again!: ")
        student_input = input(student("Student System (l/r/x) : ")).lower()
    print(sys("Logging out....."))

def gen_uniq_student_id():
    existing_ids = [s.id for s in db.students]
    while True:
        new_id = f"{random.randint(1, 999999):06}"
        if new_id not in existing_ids:
            return new_id

def register():
    print(sys(" ===== Student Registration ===== "))
    #name + email
    while True:
        firstname = input(student("What is your first name? ")).lower()
        lastname = input(student("What is your last name? ")).lower()
        email = f"{firstname}.{lastname}@university.com"

        if db.get_student_by_email(email):
            print(error("Email is already exists. Please try again with different name"))
            continue
        #validate email
        if re.match(EMAIL_PATTERN, email):
            break
        else:
            print(error("Invalid email generated. Use only letters for name (no space or numbers)"))
    print(succ(f"Your student email is: {firstname}.{lastname}@university.com"))

    #Password
    while True:
        # pwd = getpass(student("New password (Hidden): "))
        pwd = input(student("New password: "))
        if re.match(PASSWORD_PATTERN, pwd):
            break
        else:
            print(error("Invalid password format. Password must start with uppercase, have at least 5 letters and 3 digits."))
    # ID
    student_id = gen_uniq_student_id()

    print(succ("\nRegistration completed!"))
    print(succ(f"Student ID: {student_id}"))
    print(succ(f"Student Name: {firstname} {lastname}"))
    print(succ(f"Student Email: {email}"))
    print(succ(f"{pwd} Password is set and saved securely!"))

    new_student = Student(student_id, firstname, lastname, email,pwd)
    db.add_student(new_student)

    return

def login():
    print(sys(" ===== Student Login ===== "))
    while True:
        email = input(student("Enter your student email: "))
        pwd = input(student("Enter your password: "))

        if not re.match(EMAIL_PATTERN, email):
            print(error("Invalid email or password format."))
            continue

        student_obj = db.get_student_by_email(email) #Check email in DB

        if student_obj is None or student_obj.pwd != pwd:
            print(error("Incorrect email or password format. "))
            continue

        print(succ(f"\nWelcome {student_obj.firstname.capitalize()} {student_obj.lastname.capitalize()}!"))
        print(succ("You have successfully logged in! "))
        student_function(student_obj)
        return


# =========== Student Function ==========
def student_function(student_obj):
    print(sys("\n===== Student Menu ====="))
    student_input = input(student("Student Course Menu (c/e/r/s/x): ")).lower()
    while (student_input != "x"):
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
                print(student("Please try again: "))
        student_input = input(student("Student Course Menu (c/e/r/s/x): ")).lower()

    print(sys("Logging out from Student Menu..."))

def subject_enrol(student_obj):
    if len(student_obj.subject) >= 4:
        print(error("Students are allowed to enrol in 4 subjects only! "))
        return

    new_subject = Subject()
    student_obj.subject.append(new_subject)
    student_obj.update_average()
    db.save()

    print(sys(f"\nEnrolling in Subject {new_subject.id}"))
    print(sys(f"You are now enrolled in {len(student_obj.subject)} out of 4 subjects"))

def show_sub(student_obj):
    print(sys("===== Your Enrolled Subject ======"))
    if not student_obj.subject:
        print(error("Showing 0 subjects"))

    print(sys(f"Show {len(student_obj.subject)} subjects"))
    for s in student_obj.subject:
        print(sys(f"[ Subject::{s.id} -- mark = {s.mark} -- grade = {s.grade} ]"))

def sub_remove(student_obj):
    print(sys("===== Remove Subject ======"))
    if not student_obj.subject:
        print(error("You have no subjects to remove"))

    print(succ(f"Show {len(student_obj.subject)} subjects"))
    for s in student_obj.subject:
        print(sys(f"[ Subject::{s.id} -- mark = {s.mark} -- grade = {s.grade} ]"))

    subject_id = input(student("Remove Subject by ID: "))
    subject_to_remove = None
    for s in student_obj.subject:
        if s.id == subject_id:
            subject_to_remove = s

    if subject_to_remove:
        student_obj.subject.remove(subject_to_remove)
        student_obj.update_average()
        db.save()
        print(sys(f"Dropping Subject - {subject_to_remove.id}"))
        print(sys(f"You are now enrolled in {len(student_obj.subject)} out of 4 subjects"))
    else:
        print(error("Subject ID not found. Please check and try again! "))

def change_pwd(student_obj):
    while True:
        new_pwd = input(student("Enter new password: "))
        confirm_pwd = input(student("Confirm Password: "))
        if new_pwd == confirm_pwd:
            if re.match(PASSWORD_PATTERN, new_pwd):
                student_obj.pwd = new_pwd
                db.save()
                print(succ("Password changed successfully! "))
                break
            else:
                print(error(
                    "Invalid password format. Password must start with uppercase, have at least 5 letters and 3 digits."))
        else:
            print(error("The password is not match! "))

