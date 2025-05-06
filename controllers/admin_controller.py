from utils.colors import *
from models.database import Database
from models.student import *
db = Database()


def clear_db():
    print(sys("Clearing students database..."))
    CONFRIM = input(error("Are you sure you want to clear the database? (Y)es / (N)o")).lower()
    if CONFRIM == 'Y':
        db.clear()
        print(sys("Students data cleared! "))
    else:
        return

def group_grade():
    grade_order = ["HD", "D", "C", "P", "F"]
    grade_groups = {grade: [] for grade in grade_order}
    for student in db.students:
        student.update_average()
        student_grade = student.get_average_grade()
        grade_groups[student_grade].append(student)

    for grade in grade_order:
        students_in_grade = grade_groups[grade]
        if students_in_grade:
            for student in students_in_grade:
                print(
                    sys(f"{grade} --> [{student.firstname} {student.lastname} :: {student.id} --> GRADE: {grade} - MARK: {student.average_mark:.2f} ]"))
        else:
            print(sys(f"{grade} --> "))
def show_students():
    if not db.students:
        print(error("No students found in the database! "))
    else:
        print(succ(f"Showing {len(db.students)} students: "))

        for s in db.students:
            print(sys(f"[ {s.firstname} {s.lastname} :: {s.id} --> Email: {s.email} ]"))

def rm_student():
    print(sys("===== Remove Student ======"))
    if not db.students:
        print(error("You have no student to remove"))
        return

    print(succ(f"Show {len(db.students)} Students"))
    for s in db.students:
        print(sys(f"[ Student ID::{s.id} --> {s.firstname} {s.lastname} ]"))

    while True:
        student_id = input(student("Remove Student by ID: "))

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


def admin_menu():
    admin_input = input(admin("Admin System (c/g/p/r/s/x) :  " )).lower()
    while (admin_input != "x"):
        match admin_input:
            #C = Clear database on student.data
            case "c":
                clear_db()
            #G = group students by grades
            case "g":
                group_grade()
            #p = partition students: pass or fail categories
            case "p":
                pass
            #r = remove student by id
            case "r":
                rm_student()
            #s = show all students
            case "s":
               show_students()
            case _:
                print(admin("Please try again! "))
        admin_input = input(admin("Admin System (c/g/p/r/s/x) :  ")).lower()

