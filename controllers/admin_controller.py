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

def admin_menu():
    admin_input = input(admin("Admin System (c/g/p/r/s/x) :  " )).lower()
    while (admin_input != "x"):
        match admin_input:
            #C = Clear database on student.data
            case "c":
                clear_db()
            #G = group students by grades
            case "g":
                # Define grades in order (High to Low)
                grade_order = ["HD", "D", "C", "P", "F"]
                for grade in grade_order:
                    has_student = False  # check if there is student for this grade

                    for student in db.students:
                        student.update_average()  # update student's average before check
                        student_grade = student.get_student_grade(student.average_mark)

                        if student_grade == grade:
                            has_student = True
                            print(
                                sys(f"{grade} --> [ {student.firstname.capitalize()} {student.lastname.capitalize()} :: {student.id} --> Email: {student.email} --> AVG MARK: {student.average_mark:.2f} ]"))

                    if not has_student:
                        print(sys(f"{grade} -->"))
            #p = partition students: pass or fail categories
            case "p":
                pass
            #r = remove student by id
            case "r":
                pass
            #s = show all students
            case "s":
                if not db.students:
                    print(error("No students found in the database! "))
                else:
                    print(succ(f"Showing {len(db.students)} students: "))

                    for s in db.students:
                        print(sys(f"[ {s.firstname} {s.lastname} :: {s.id} --> Email: {s.email} ]"))
            case _:
                print(admin("Please try again! "))
        admin_input = input(admin("Admin System (c/g/p/r/s/x) :  ")).lower()

