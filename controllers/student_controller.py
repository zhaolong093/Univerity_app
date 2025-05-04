import re
import random
from getpass import getpass
from utils.colors import *
from models.database import Database
from models.student import Student



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

def register():
    print(" ===== Student Registration ===== ")
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
    new_id = f"{random.randint(1, 999999):06}"
    student_id = new_id

    print(succ("\nRegistration completed!"))
    print(succ(f"Student ID: {new_id}"))
    print(succ(f"Student Name: {firstname} {lastname}"))
    print(succ(f"Student Email: {email}"))
    print(succ(f"{pwd}Password is set and saved securely!"))

    new_student = Student(student_id, firstname, lastname, email,pwd)
    db.add_student(new_student)

    return

def login():
    print(" ===== Student Login ===== ")

    email = input(student("Enter your student email: "))
    student_obj = db.get_student_by_email(email) #Check email in DB

    if student_obj is None:
        print(error("Email not found. Please register or check your email."))
        return

    pwd  = input(student("Enter your password: "))

    if student_obj.pwd == pwd:
        print(succ(f"\nWelcome {student_obj.firstname.capitalize()} {student_obj.lastname.capitalize()}!"))
        print(succ("You have successfully logged in! "))
        student_function(student_obj)
    else:
        print(error("Incorrect email or password. Please try again! "))

# =========== Student Menu ==========
def student_function(student_obj):
    print(student("\n===== Student Menu ====="))
    student_input = input(student("Student Course Menu (c/e/r/s/x): ")).lower()
    while (student_input != "x"):
        match student_input:
            case "c":
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
                            print(error("Invalid password format. Password must start with uppercase, have at least 5 letters and 3 digits."))
                    else:
                        print("The password is not match! ")
            case "e":
                pass
            case "r":
                pass
            case "s":
                pass
            case _:
                print(student("Please try again: "))
        student_input = input(student("Student Course Menu (c/e/r/s/x): ")).lower()

    print(start("Logging out from Student Menu..."))

