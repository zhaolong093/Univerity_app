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
   pass


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
                pass
            #s = show all students
            case "s":
               show_students()
            case _:
                print(admin("Please try again! "))
        admin_input = input(admin("Admin System (c/g/p/r/s/x) :  ")).lower()

