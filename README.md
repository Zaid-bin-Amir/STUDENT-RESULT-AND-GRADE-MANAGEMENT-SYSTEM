# Student Result & Grade Management System

A console-based Python application to manage student details, subject marks, grades and academic performance.

## Features

- Add new students with subject-wise marks
- Update marks, add new subjects or change a student's name
- Search students by roll number or name
- View all students ranked by percentage
- Detailed report card for each student
- Class performance summary (average, topper, lowest scorer, pass/fail count, grade distribution)
- Delete student records
- Data saved automatically in `students.json`

## Project Structure

| File | Purpose |
|------|---------|
| `main.py` | Menu and user interaction |
| `students.py` | Student operations: add, update, search, summary |
| `grades.py` | Total, percentage, grade and pass/fail calculation |
| `storage.py` | Load and save data to JSON |
| `students.json` | Sample data (3 students) |

## Requirements

- Python 3.8 or higher
- No external libraries needed
- No dataset needed, records are entered by the user

## How to Run

```bash
python main.py
```

On some systems use `python3 main.py`.

## Grading Scale

| Percentage | Grade |
|-----------|-------|
| 90 and above | A+ |
| 80 - 89 | A |
| 70 - 79 | B |
| 60 - 69 | C |
| 50 - 59 | D |
| Below 50 | F |

A student passes with 50% or more overall.

## Menu Options

1. Add student
2. Update student
3. Search student
4. View all students
5. View report card
6. Class performance summary
7. Delete student
0. Exit

## Concepts Covered

Variables, data types, conditions, loops, functions, lists, dictionaries, file handling with JSON, modular application design.

## Sample Output

```
======================================================================
                         ALL STUDENTS
======================================================================
Roll    Name                      Total   Percent   Grade   Status
----------------------------------------------------------------------
102     Sara Ahmed                273.0    91.00%      A+     Pass
101     Ali Khan                  255.0    85.00%       A     Pass
103     Hamza                     157.0    52.33%       D     Pass
```

## Git Usage

```bash
git init
git add .
git commit -m "Student Result & Grade Management System"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```
