
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="📊",
    layout="wide"
)

if "students" not in st.session_state:
    st.session_state.students = []

st.title("📊 Student Performance Analyzer")
st.write("Analyze student marks and academic performance.")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page",
    ["Dashboard", "Add Student", "Student Records"]
)

if page == "Add Student":
    st.header("Add Student Details")

    with st.form("student_form"):
        name = st.text_input("Student Name")
        subject_count = st.number_input(
            "Number of subjects",
            min_value=1,
            max_value=10,
            value=3
        )

        subjects = {}
        for i in range(int(subject_count)):
            subject = st.text_input(
                f"Subject {i + 1}",
                key=f"subject_{i}"
            )
            mark = st.number_input(
                f"Marks for Subject {i + 1}",
                min_value=0,
                max_value=100,
                value=0,
                key=f"mark_{i}"
            )
            subjects[subject.strip()] = mark

        submitted = st.form_submit_button("Add Student")

        if submitted:
            if not name.strip():
                st.error("Please enter the student name.")
            elif any(not subject for subject in subjects):
                st.error("Please enter all subject names.")
            elif len(subjects) != int(subject_count):
                st.error("Subject names must be unique.")
            elif len(st.session_state.students) > 0 and any(
                s["name"].lower() == name.strip().lower()
                for s in st.session_state.students
            ):
                st.error("This student name already exists.")
            else:
                total = sum(subjects.values())
                average = total / len(subjects)
                status = (
                    "PASS"
                    if all(mark >= 35 for mark in subjects.values())
                    else "NEEDS IMPROVEMENT"
                )

                st.session_state.students.append({
                    "name": name.strip(),
                    "marks": subjects,
                    "total": total,
                    "average": average,
                    "status": status
                })

                st.success("Student added successfully!")

elif page == "Dashboard":
    st.header("Performance Overview")

    students = st.session_state.students

    if not students:
        st.info("No student records yet. Go to Add Student to begin.")
    else:
        total_students = len(students)
        avg = sum(s["average"] for s in students) / total_students
        passed = sum(s["status"] == "PASS" for s in students)
        needs_improvement = total_students - passed

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Students", total_students)
        col2.metric("Average Performance", f"{avg:.2f}%")
        col3.metric("Passed", passed)
        col4.metric("Needs Improvement", needs_improvement)

        st.subheader("Student Average Marks")

        chart_data = pd.DataFrame({
            "Student": [s["name"] for s in students],
            "Average Marks": [s["average"] for s in students]
        })

        st.bar_chart(
            chart_data,
            x="Student",
            y="Average Marks"
        )

        st.subheader("Performance Summary")

        for student in students:
            st.write(
                f"**{student['name']}** — "
                f"{student['average']:.2f}% — "
                f"{student['status']}"
            )

elif page == "Student Records":
    st.header("All Student Records")

    students = st.session_state.students

    if not students:
        st.info("No records available. Add a student first.")
    else:
        records = []

        for student in students:
            records.append({
                "Name": student["name"],
                "Total": student["total"],
                "Average": round(student["average"], 2),
                "Status": student["status"]
            })

        st.dataframe(
            pd.DataFrame(records),
            use_container_width=True
        )

        selected = st.selectbox(
            "View individual student report",
            [s["name"] for s in students]
        )

        student = next(
            s for s in students if s["name"] == selected
        )

        st.subheader(f"Report: {student['name']}")
        st.write("Subject Marks:", student["marks"])
        st.write("Total:", student["total"])
        st.write("Average:", round(student["average"], 2))
        st.write("Status:", student["status"])
