from grades import build_result
from storage import load_students, save_students
from students import (
    add_student,
    class_summary,
    delete_student,
    ranked_students,
    search_by_name,
    search_by_roll,
    update_marks,
    update_name,
)

DEFAULT_SUBJECTS = ["Math", "English", "Science"]
LINE = "=" * 70


def read_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def read_mark(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if 0 <= value <= 100:
            return int(value) if value.is_integer() else value
        print("Marks must be between 0 and 100.")


def read_subjects():
    default_text = ", ".join(DEFAULT_SUBJECTS)
    raw = input(f"Subjects separated by comma [{default_text}]: ").strip()
    if not raw:
        return list(DEFAULT_SUBJECTS)
    subjects = []
    for item in raw.split(","):
        item = item.strip()
        if item and item.lower() not in [s.lower() for s in subjects]:
            subjects.append(item)
    return subjects or list(DEFAULT_SUBJECTS)


def print_header(title):
    print()
    print(LINE)
    print(title.center(70))
    print(LINE)


def print_table(entries):
    if not entries:
        print("No records found.")
        return
    print(f"{'Roll':<8}{'Name':<22}{'Total':>8}{'Percent':>10}{'Grade':>8}{'Status':>9}")
    print("-" * 70)
    for roll, data, result in entries:
        print(
            f"{roll:<8}{data['name'][:20]:<22}{result['total']:>8.1f}"
            f"{result['percentage']:>9.2f}%{result['grade']:>8}{result['status']:>9}"
        )


def entries_from(students):
    return [(roll, data, build_result(data)) for roll, data in students.items()]


def print_report_card(roll, data):
    result = build_result(data)
    print_header("REPORT CARD")
    print(f"Name       : {data['name']}")
    print(f"Roll No    : {roll}")
    print("-" * 70)
    print(f"{'Subject':<30}{'Marks':>10}")
    print("-" * 70)
    for subject, mark in data["marks"].items():
        print(f"{subject:<30}{mark:>10}")
    print("-" * 70)
    print(f"{'Total':<30}{result['total']:>10.1f}")
    print(f"{'Percentage':<30}{result['percentage']:>9.2f}%")
    print(f"{'Grade':<30}{result['grade']:>10}")
    print(f"{'Status':<30}{result['status']:>10}")
    print(LINE)


def handle_add(students):
    print_header("ADD STUDENT")
    roll = read_text("Roll number: ")
    if roll in students:
        print("A student with this roll number already exists.")
        return
    name = read_text("Student name: ")
    marks = {}
    for subject in read_subjects():
        marks[subject] = read_mark(f"Marks in {subject} (0-100): ")
    add_student(students, roll, name, marks)
    save_students(students)
    print(f"Student {name} added successfully.")


def handle_update(students):
    print_header("UPDATE STUDENT")
    roll = read_text("Roll number: ")
    if roll not in students:
        print("Student not found.")
        return
    data = students[roll]
    print(f"Selected: {data['name']}")
    print("1. Update marks of a subject")
    print("2. Change student name")
    choice = input("Choose an option: ").strip()
    if choice == "1":
        print("Current subjects:", ", ".join(data["marks"]))
        subject = read_text("Subject name: ")
        mark = read_mark(f"New marks for {subject} (0-100): ")
        outcome = update_marks(students, roll, subject, mark)
        save_students(students)
        print(f"Subject {outcome} successfully.")
    elif choice == "2":
        name = read_text("New name: ")
        update_name(students, roll, name)
        save_students(students)
        print("Name updated successfully.")
    else:
        print("Invalid option.")


def handle_search(students):
    print_header("SEARCH STUDENT")
    print("1. Search by roll number")
    print("2. Search by name")
    choice = input("Choose an option: ").strip()
    if choice == "1":
        found = search_by_roll(students, read_text("Roll number: "))
    elif choice == "2":
        found = search_by_name(students, read_text("Name or part of name: "))
    else:
        print("Invalid option.")
        return
    if not found:
        print("No matching student found.")
        return
    if len(found) == 1:
        roll, data = next(iter(found.items()))
        print_report_card(roll, data)
    else:
        print_table(entries_from(found))


def handle_view_all(students):
    print_header("ALL STUDENTS")
    print_table(ranked_students(students))


def handle_report_card(students):
    roll = read_text("Roll number: ")
    if roll not in students:
        print("Student not found.")
        return
    print_report_card(roll, students[roll])


def handle_summary(students):
    print_header("CLASS PERFORMANCE SUMMARY")
    summary = class_summary(students)
    if not summary:
        print("No student records available.")
        return
    topper = students[summary["topper"]]["name"]
    lowest = students[summary["lowest"]]["name"]
    print(f"Total students   : {summary['count']}")
    print(f"Class average    : {summary['average']:.2f}%")
    print(f"Topper           : {topper} (Roll {summary['topper']}) - {summary['topper_percentage']:.2f}%")
    print(f"Lowest scorer    : {lowest} (Roll {summary['lowest']}) - {summary['lowest_percentage']:.2f}%")
    print(f"Passed           : {summary['passed']}")
    print(f"Failed           : {summary['failed']}")
    print("Grade distribution:")
    for grade in ["A+", "A", "B", "C", "D", "F"]:
        count = summary["grade_counts"].get(grade, 0)
        print(f"  {grade:<3}: {'#' * count} {count}")
    print(LINE)


def handle_delete(students):
    print_header("DELETE STUDENT")
    roll = read_text("Roll number: ")
    if roll not in students:
        print("Student not found.")
        return
    confirm = input(f"Delete {students[roll]['name']}? (y/n): ").strip().lower()
    if confirm == "y":
        delete_student(students, roll)
        save_students(students)
        print("Student deleted.")
    else:
        print("Deletion cancelled.")


def show_menu():
    print_header("STUDENT RESULT & GRADE MANAGEMENT SYSTEM")
    print("1. Add student")
    print("2. Update student")
    print("3. Search student")
    print("4. View all students")
    print("5. View report card")
    print("6. Class performance summary")
    print("7. Delete student")
    print("0. Exit")


def main():
    students = load_students()
    actions = {
        "1": handle_add,
        "2": handle_update,
        "3": handle_search,
        "4": handle_view_all,
        "5": handle_report_card,
        "6": handle_summary,
        "7": handle_delete,
    }
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(students)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
