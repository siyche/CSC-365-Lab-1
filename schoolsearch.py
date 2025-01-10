import os

def load_students(file_path):
    """Load student data from the given file."""
    students = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                fields = line.strip().split(',')
                if len(fields) != 8:
                    print(f"Invalid line: {line.strip()}")  # Debugging line
                    raise ValueError("Invalid file format.")

                student = {
                    'last_name': fields[0],
                    'first_name': fields[1],
                    'grade': int(fields[2]),
                    'classroom': int(fields[3]),
                    'bus': int(fields[4]),
                    'gpa': float(fields[5]),
                    'teacher_last_name': fields[6],
                    'teacher_first_name': fields[7]
                }
                students.append(student)
        return students
    except FileNotFoundError:
        print("Error: File not found.")
        exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

def search_students_by_last_name(students, last_name, bus=False):
    results = []
    for student in students:
        if student['last_name'] == last_name:
            if bus:
                results.append(f"{student['last_name']}, {student['first_name']}, Bus Route: {student['bus']}")
            else:
                results.append(f"{student['last_name']}, {student['first_name']}, Grade: {student['grade']}, Classroom: {student['classroom']}, Teacher: {student['teacher_last_name']} {student['teacher_first_name']}")
    return results

def search_students_by_teacher(students, teacher_last_name):
    return [f"{s['last_name']}, {s['first_name']}" for s in students if s['teacher_last_name'] == teacher_last_name]

def search_students_by_bus(students, bus_route):
    return [f"{s['last_name']}, {s['first_name']}, Grade: {s['grade']}, Classroom: {s['classroom']}" for s in students if s['bus'] == bus_route]

def search_students_by_grade(students, grade):
    return [f"{s['last_name']}, {s['first_name']}" for s in students if s['grade'] == grade]

def grade_average_gpa(students, grade):
    grade_students = [s['gpa'] for s in students if s['grade'] == grade]
    if grade_students:
        return round(sum(grade_students) / len(grade_students), 2)
    return None

def grade_high_low_gpa(students, grade, high=True):
    grade_students = [s for s in students if s['grade'] == grade]
    if not grade_students:
        return None
    key_func = max if high else min
    student = key_func(grade_students, key=lambda s: s['gpa'])
    return f"{student['last_name']}, {student['first_name']}, GPA: {student['gpa']}, Teacher: {student['teacher_last_name']} {student['teacher_first_name']}, Bus: {student['bus']}"

def info_summary(students):
    grade_counts = {grade: 0 for grade in range(7)}
    for student in students:
        grade_counts[student['grade']] += 1
    return [f"Grade {grade}: {count} Students" for grade, count in sorted(grade_counts.items())]

def main():
    file_path = "students.txt"
    students = load_students(file_path)

    while True:
        command = input("Enter command: ").strip()
        if command.startswith('S:'):
            parts = command.split()
            last_name = parts[1]
            bus = len(parts) > 2 and parts[2] == 'B'
            results = search_students_by_last_name(students, last_name, bus)
            print("\n".join(results) if results else "No students found.")

        elif command.startswith('T:'):
            teacher_last_name = command[2:].strip()
            results = search_students_by_teacher(students, teacher_last_name)
            print("\n".join(results) if results else "No students found.")

        elif command.startswith('B:'):
            bus_route = int(command[2:].strip())
            results = search_students_by_bus(students, bus_route)
            print("\n".join(results) if results else "No students found.")

        elif command.startswith('G:'):
            parts = command.split()
            grade = int(parts[1])
            if len(parts) > 2:
                if parts[2] == 'H':
                    result = grade_high_low_gpa(students, grade, high=True)
                elif parts[2] == 'L':
                    result = grade_high_low_gpa(students, grade, high=False)
                else:
                    result = "Invalid command."
                print(result if result else "No students found.")
            else:
                results = search_students_by_grade(students, grade)
                print("\n".join(results) if results else "No students found.")

        elif command.startswith('A:'):
            grade = int(command[2:].strip())
            avg = grade_average_gpa(students, grade)
            print(f"Grade {grade} Average GPA: {avg}" if avg is not None else "No students found.")

        elif command == 'I':
            summary = info_summary(students)
            print("\n".join(summary))

        elif command == 'Q':
            break

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()