from utils.colors import *
from models.database import Database

db = Database()

def clear_db():
    print(sys("\tClearing students database..."))
    while True:
        CONFIRM = input(error("\tAre you sure you want to clear the database? (Y)es / (N)o: ")).lower()
        if CONFIRM == 'y':
            try:
                db.clear()
                print(sys("\tStudents data cleared! "))
            except Exception as e:
                print(error(f"\tFailed to clear students data. Errors: {str(e)}"))
            return
        elif CONFIRM == 'n':
            print(sys("\tCancelled. Database was not cleared."))
            break
        else:
            print(error("\tInvalid option. Please enter Y or N."))


def group_grade():
    print(sys("\tGrade Grouping"))
    grade_order = ["HD", "D", "C", "P", "F"]
    grade_groups = {grade: [] for grade in grade_order}
    students = db.load()

    if not students:
        print(error("\t< Nothing to display >"))

    for student in students:
        student.update_average()
        student_grade = student.get_average_grade()
        grade_groups[student_grade].append(student)

    for grade in grade_order:
        students_in_grade = grade_groups[grade]

        if students_in_grade:
            for student in students_in_grade:
                print(
                    sys(f"\t{grade} --> [{student.firstname} {student.lastname} :: {student.id} --> GRADE: {grade} - MARK: {student.average_mark:.2f} ]"))
        # else:




def show_students():
    students = db.load()
    if not students:
        print(sys(f"\tStudents List: {len(students)} "))
        print(error("\t< Nothing to Display >"))
    else:
        print(sys(f"\tStudents List: {len(students)} "))
        for s in students:
            print(sys(f"\t{s.firstname} {s.lastname:} :: {s.id} --> Email: {s.email} "))

def rm_student():
    # print(sys("===== Remove Student ======"))
    students = db.load()
    if not students:
        print(error("\tYou have no student to remove"))
        return

    print(succ(f"\tShow Students :  {len(students)} "))
    for s in students:
        print(sys(f"\t[ Student ID::{s.id} --> {s.firstname} {s.lastname} ]"))

    while True:
        student_id = input(student("\tRemove Student by ID: "))
        if student_id == 'x':
            return

        # validate the input by exactly 6 digit
        if not student_id.isdigit() or len(student_id) !=6:
            print(error("\tInvalid ID format! Please enter 6-digit number! "))
            continue
        #find student
        student_to_remove = next((s for s in db.students if s.id == student_id), None)
        #easy version here:
        # for s in db.students:
        #     if s.id == student_id:
        #         student_to_remove = s

        if student_to_remove:
            confirm = input(error(f"\tAre you sure to remove {student_to_remove.id} --> {student_to_remove.firstname} {student_to_remove.lastname} (y/n)? ")).lower()
            if confirm == 'y':
                db.students.remove(student_to_remove)
                db.save()
                print(sys(f"\tRemoving Student {student_to_remove.id} Account"))
            else:
                print(sys("\tCancelled removal."))
            break
        else:
            print(error(f"\tStudent {student_id} does not exist!"))
            # print(error("Student ID not found. Please check and try again! "))

def partition_student():
    print(sys("\tPASS / FAIL Partition"))
    students = db.load()
    pass_student = []
    fail_student = []

    for student in students:
        student.update_average()
        info = f"{student.firstname} {student.lastname} :: {student.id} --> GRADE : {student.get_average_grade()} -- MARK : {student.average_mark:.2f} "
        if student.is_pass():
            pass_student.append(info)
        else:
            fail_student.append(info)

    #New version
    if fail_student:
        print(sys(f"\tFAIL --> [{', '.join(fail_student)}]"))
    else:
        print(sys(f"\tFAIL --> []"))

    if pass_student:
        print(sys(f"\tPASS --> [{', '.join(pass_student)}]"))
    else:
        print(sys(f"\tPASS --> []"))

    #old version
    # if fail_student:
    #     # print(admin(fail_student.append(student)))
    #     for s in fail_student:
    #         print(sys(f"\tFAIL --> [ {s.firstname} {s.lastname} :: {s.id} --> GRADE : {s.get_average_grade()} - MARK: {s.average_mark:.2f} ]"))
    # else:
    #     print(sys("\tFAIL --> []"))
    #
    # if pass_student:
    #     # print(admin(pass_student.append(student)))
    #     for s in pass_student:
    #         print(sys(f"\tPASS --> [ {s.firstname} {s.lastname} :: {s.id} --> GRADE : {s.get_average_grade()} - MARK: {s.average_mark:.2f} ]"))
    # else:
    #     print(sys("\tPASS --> []"))

def admin_menu():
    admin_input = input(admin("\tAdmin System (c/g/p/r/s/x) :  " )).lower()
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
                    print(admin("\tPlease try again! "))
            admin_input = input(admin("\tAdmin System (c/g/p/r/s/x) :  ")).lower()
        except Exception as e:
            print(error(f"\tAn unexpected error occurred: {str(e)}"))