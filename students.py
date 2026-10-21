from grades import build_result


def add_student(students, roll, name, marks):
    if roll in students:
        return False
    students[roll] = {"name": name, "marks": marks}
    return True


def delete_student(students, roll):
    if roll not in students:
        return False
    del students[roll]
    return True


def find_subject(student, subject):
    for existing in student["marks"]:
        if existing.lower() == subject.lower():
            return existing
    return None


def update_marks(students, roll, subject, mark):
    if roll not in students:
        return None
    student = students[roll]
    existing = find_subject(student, subject)
    if existing:
        student["marks"][existing] = mark
        return "updated"
    student["marks"][subject] = mark
    return "added"


def update_name(students, roll, name):
    if roll not in students:
        return False
    students[roll]["name"] = name
    return True


def search_by_roll(students, roll):
    if roll in students:
        return {roll: students[roll]}
    return {}


def search_by_name(students, query):
    query = query.lower()
    return {
        roll: data
        for roll, data in students.items()
        if query in data["name"].lower()
    }


def class_summary(students):
    if not students:
        return None

    results = {roll: build_result(data) for roll, data in students.items()}
    percentages = [result["percentage"] for result in results.values()]

    topper = max(results, key=lambda roll: results[roll]["percentage"])
    lowest = min(results, key=lambda roll: results[roll]["percentage"])

    grade_counts = {}
    for result in results.values():
        grade_counts[result["grade"]] = grade_counts.get(result["grade"], 0) + 1

    passed = sum(1 for result in results.values() if result["status"] == "Pass")

    return {
        "count": len(students),
        "average": sum(percentages) / len(percentages),
        "topper": topper,
        "topper_percentage": results[topper]["percentage"],
        "lowest": lowest,
        "lowest_percentage": results[lowest]["percentage"],
        "passed": passed,
        "failed": len(students) - passed,
        "grade_counts": grade_counts,
    }


def ranked_students(students):
    results = {roll: build_result(data) for roll, data in students.items()}
    order = sorted(results, key=lambda roll: results[roll]["percentage"], reverse=True)
    return [(roll, students[roll], results[roll]) for roll in order]
