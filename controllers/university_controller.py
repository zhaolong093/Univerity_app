from controllers.admin_controller import admin_menu
from controllers.student_controller import student_menu
from utils.colors import *


def university_menu():
    userInput = input(sys("University system: (A)dmin, (S)tudent, or X : ")).lower()
    while (userInput != "x"):
        match userInput:
            case "a":
                admin_menu()
            case "s":
                student_menu()
            case _:
                print("Please try again!: ")
        userInput = input("University system: (A)dmin, (S)tudent, or X : ")

