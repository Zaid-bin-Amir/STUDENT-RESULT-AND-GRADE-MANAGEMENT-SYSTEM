PASS_PERCENTAGE = 50

GRADE_SCALE = [
    (90, "A+"),
    (80, "A"),
    (70, "B"),
    (60, "C"),
    (50, "D"),
    (0, "F"),
]


def calculate_total(marks):
    return sum(marks.values())


def calculate_percentage(marks):
    if not marks:
        return 0.0
    return calculate_total(marks) / len(marks)


def get_grade(percentage):
    for minimum, grade in GRADE_SCALE:
        if percentage >= minimum:
            return grade
    return "F"


def get_status(percentage):
    return "Pass" if percentage >= PASS_PERCENTAGE else "Fail"


def build_result(student):
    marks = student["marks"]
    percentage = calculate_percentage(marks)
    return {
        "total": calculate_total(marks),
        "percentage": percentage,
        "grade": get_grade(percentage),
        "status": get_status(percentage),
    }
