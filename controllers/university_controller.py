from controllers.admin_controller import admin_menu
from controllers.student_controller import student_menu


def university_menu():
    userInput = input("University system: (A)dmin, (S)tudent, or X : ")
    while (userInput != "x"):
        match userInput:
            case "a":
                admin_menu()
            case "s":
                student_menu()
            case _:
                print("University system: (A)dmin, (S)tudent, or X: ")

