import re
import random
from getpass import getpass
from utils.colors import *
from models.database import Database



#use r'' = for writing regex
# $ = mean end of string
EMAIL_PATTERN = r'^[a-z]+\.[a-z]+@university\.com$'
PASSWORD_PATTERN = r'^[A-Z][a-zA-Z]{5,}\d{3,}$'
db = Database()



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
                print("Please try again! Student System (l/r/x) : ")
        student_input = input(student("Student System (l/r/x) : ")).lower()

def gen_uniq_student_id():
    existing_ids = {student.id for student in db.students}
    while True:
        new_id = f"{random.randint(1, 999999):06}"
        if new_id not in db:
            return new_id

def register():
    print(" ===== Student Registration ===== ")
    #name + email
    while True:
        firstname = input(student("What is your first name? ")).lower()
        lastname = input(student("What is your last name? ")).lower()
        email = f"{firstname}.{lastname}@university.com"

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



    print(succ("\nRegistration completed!"))
    print(succ(f"Student Name: {firstname} {lastname}"))
    print(succ(f"Student Email: {email}"))
    print(succ("Password is set and saved securely!"))
    return

def login():
    pass