students = []

def add_students(name, student_id=22):
    student = {"name": name, "student_id": student_id}
    students.append(name)

student_name = input("Enter student name:")

add_students(student_name)
print(students)


