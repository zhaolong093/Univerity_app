from utils.colors import *


def admin_menu():
    admin_input = input(admin("Admin System (c/g/p/r/s/x) :  " )).lower()
    while (admin_input != "x"):
        match admin_input:
            #C = Clear database on student.data
            case "c":
                pass
            #G = group students by grades
            case "g":
                pass
            #p = partition students: pass or fail categories
            case "p":
                pass
            #r = remove student by id
            case "r":
                pass
            #s = show all students
            case "s":
                pass
            case _:
                pass