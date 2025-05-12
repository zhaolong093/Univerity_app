from utils.colors import *
from models.database import Database

db = Database()


def clear_db():
    print(sys("Clearing students database..."))
    while True:
        CONFIRM = input(error("Are you sure you want to clear the database? (Y)es / (N)o: ")).lower()
        if CONFIRM == 'y':
            try:
                db.clear()
                print(sys("Students data cleared! "))
            except Exception as e:
                print(error(f"Failed to clear students data. Errors: {str(e)}"))
            return
        elif CONFIRM == 'n':
            print(sys("Cancelled. Database was not cleared."))
            break
        else:
            print(error("Invalid option. Please enter Y or N."))


def group_grade():
    grade_order = ["HD", "D", "C", "P", "F"]
    grade_groups = {grade: [] for grade in grade_order}
    students = db.load()
    for student in students:
        student.update_average()
        student_grade = student.get_average_grade()
        grade_groups[student_grade].append(student)


    for grade in grade_order:
        students_in_grade = grade_groups[grade]
        print("Grade Grouping")
        if students_in_grade:
            for student in students_in_grade:
                print(
                    sys(f"{grade} --> [{student.firstname} {student.lastname} :: {student.id} --> GRADE: {grade} - MARK: {student.average_mark:.2f} ]"))
        else:
            print(sys(f"{grade} --> "))
def show_students():
    students = db.load()
    if not students:
        print(succ(f"Students List: {len(db.students)} "))
        print(error("< Nothing to Display >"))
    else:
        print(succ(f"Students List: {len(db.students)} "))
        for s in students:
            print(sys(f"[ {s.firstname} {s.lastname} :: {s.id} --> Email: {s.email} ]"))

def rm_student():
    print(sys("===== Remove Student ======"))
    students = db.load()
    if not students:
        print(error("You have no student to remove"))
        return

    print(succ(f"Show {len(db.students)} Students"))
    for s in students:
        print(sys(f"[ Student ID::{s.id} --> {s.firstname} {s.lastname} ]"))

    while True:
        student_id = input(student("Remove Student by ID: "))
        if student_id == 'x':
            return

        # validate the input by exactly 6 digit
        if not student_id.isdigit() or len(student_id) !=6:
            print(error("Invalid ID format! Please enter 6-digit number! "))
            continue
        #find student
        student_to_remove = next((s for s in db.students if s.id == student_id), None)
        #easy version here:
        # for s in db.students:
        #     if s.id == student_id:
        #         student_to_remove = s

        if student_to_remove:
            confirm = input(error(f"Are you sure to remove {student_to_remove.id} --> {student_to_remove.firstname} {student_to_remove.lastname} (y/n)? ")).lower()
            if confirm == 'y':
                db.students.remove(student_to_remove)
                db.save()
                print(sys(f"Dropping Student - {student_to_remove.id}"))
            else:
                print(sys("Cancelled removal."))
            break
        else:
            print(error("Student ID not found. Please check and try again! "))

def partition_student():
    print(sys("PASS / FAIL Partition"))
    students = db.load()
    pass_student = []
    fail_student = []

    for student in students:
        student.update_average()
        if student.is_pass():
            pass_student.append(student)
        else:
            fail_student.append(student)

    if fail_student:
        # print(admin(fail_student.append(student)))
        for s in fail_student:
            print(sys(f"FAIL --> [ {s.firstname} {s.lastname} :: {s.id} --> GRADE : {s.get_average_grade()} - MARK: {s.average_mark:.2f} ]"))
    else:
        print(sys("FAIL --> []"))

    if pass_student:
        # print(admin(pass_student.append(student)))
        for s in pass_student:
            print(sys(f"PASS --> [ {s.firstname} {s.lastname} :: {s.id} --> GRADE : {s.get_average_grade()} - MARK: {s.average_mark:.2f} ]"))
    else:
        print(sys("PASS --> []"))

def admin_menu():
    admin_input = input(admin("Admin System (c/g/p/r/s/x) :  " )).lower()
    while (admin_input != "x"):
        try:
            match admin_input:
                #C = Clear database on student.data
                case "c":
                    clear_db()
                #G = group students by grades
                case "g":
                    group_grade()
                #p = partition students: pass or fail categories
                case "p":
                    partition_student()
                #r = remove student by id
                case "r":
                    rm_student()
                #s = show all students
                case "s":
                   show_students()
                case _:
                    print(admin("Please try again! "))
            admin_input = input(admin("Admin System (c/g/p/r/s/x) :  ")).lower()
        except Exception as e:
            print(error(f"An unexpected error occurred: {str(e)}"))