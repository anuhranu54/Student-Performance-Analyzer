
# STUDENT PERFORMANCE ANALYZER
# Minor Project using Python

PASS_MARK = 35

# List to store multiple student records
students = []


# Function to accept valid marks
def get_marks(subject):
    while True:
        try:
            marks = int(input(f"Enter marks for {subject} (0-100): "))

            if 0 <= marks <= 100:
                return marks
            else:
                print("Invalid! Marks must be between 0 and 100.")

        except ValueError:
            print("Please enter numbers only.")


# Function to calculate performance
def calculate_performance(marks):
    total = sum(marks.values())
    average = total / len(marks)
    highest = max(marks.values())
    lowest = min(marks.values())

    if all(mark >= PASS_MARK for mark in marks.values()):
        status = "PASS"
    else:
        status = "NEEDS IMPROVEMENT"

    return {
        "total": total,
        "average": average,
        "highest": highest,
        "lowest": lowest,
        "status": status
    }


# Function to add a student
def add_student():
    print("\n--- ADD STUDENT ---")

    name = input("Enter student name: ").strip()

    if not name:
        print("Name cannot be empty!")
        return

    while True:
        try:
            count = int(input("Enter number of subjects: "))
            if count > 0:
                break
            print("Enter at least one subject.")
        except ValueError:
            print("Enter a valid number.")

    marks = {}

    for i in range(count):
        subject = input(f"Enter subject {i + 1} name: ").strip()

        while not subject or subject in marks:
            if not subject:
                print("Subject name cannot be empty.")
            else:
                print("Subject already entered.")

            subject = input("Enter subject name again: ").strip()

        marks[subject] = get_marks(subject)

    performance = calculate_performance(marks)

    student = {
        "name": name,
        "marks": marks,
        "performance": performance
    }

    students.append(student)

    print("\nStudent added successfully!")


# Function to display one student's report
def display_report(student):
    print("\n========== STUDENT REPORT ==========")

    print("Student Name:", student["name"])
    print("\nSubject Marks:")

    for subject, mark in student["marks"].items():
        print(subject, ":", mark)

    result = student["performance"]

    print("\nTotal Marks:", result["total"])
    print("Average Marks:", round(result["average"], 2))
    print("Highest Marks:", result["highest"])
    print("Lowest Marks:", result["lowest"])
    print("Status:", result["status"])

    print("====================================")


# Function to display all students
def display_all_students():
    if len(students) == 0:
        print("\nNo student records available.")
        return

    for student in students:
        display_report(student)


# Main function
def main():
    while True:
        print("\n===== STUDENT PERFORMANCE ANALYZER =====")
        print("1. Add Student")
        print("2. View All Student Reports")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            display_all_students()

        elif choice == "3":
            print("\nThank you for using the application!")
            break

        else:
            print("Invalid choice! Try again.")


# Execute application
if __name__ == "__main__":
    main()
