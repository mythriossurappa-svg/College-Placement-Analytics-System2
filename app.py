import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
df = pd.read_csv("placements.csv")

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "student" not in st.session_state:
    st.session_state.student = None

# LOGIN PAGE
if not st.session_state.logged_in:

    st.title("🎓 College Placement Analytics System")

    st.subheader("Student Login")

    roll_no = st.text_input("Roll Number")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        student = df[
            (df["roll_no"] == roll_no)
            & (df["password"].astype(str) == password)
        ]

        if len(student) > 0:
            st.session_state.logged_in = True
            st.session_state.student = student.iloc[0]
            st.rerun()
        else:
            st.error("Invalid Roll Number or Password")

    st.stop()

# STUDENT DASHBOARD
student = st.session_state.student

st.sidebar.success("Logged In")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.title("🎓 Student Placement Dashboard")

st.subheader("Student Information")

col1, col2 = st.columns(2)

with col1:
    st.write("**Name:**", student["student_name"])
    st.write("**Roll No:**", student["roll_no"])
    st.write("**Department:**", student["department"])

with col2:
    st.write("**CGPA:**", student["cgpa"])
    st.write("**Placement Status:**", student["placement_status"])
    st.write("**Company:**", student["company_name"])

st.markdown("---")

# ANALYTICS SECTION

st.header("Placement Analytics")

total_students = len(df)
placed_students = len(df[df["placement_status"] == "Placed"])

placement_percentage = round(
    placed_students / total_students * 100,
    2
)

average_package = round(
    df["package_lpa"].mean(),
    2
)

highest_package = df["package_lpa"].max()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Students", total_students)
c2.metric("Placed Students", placed_students)
c3.metric("Placement %", placement_percentage)
c4.metric("Highest Package", highest_package)

# Department Chart
dept = df.groupby(
    "department"
).size().reset_index(name="count")

fig1 = px.bar(
    dept,
    x="department",
    y="count",
    title="Department-wise Placements"
)

st.plotly_chart(fig1)

# Placement Status Pie Chart
status = (
    df["placement_status"]
    .value_counts()
    .reset_index()
)

status.columns = [
    "status",
    "count"
]

fig2 = px.pie(
    status,
    names="status",
    values="count",
    title="Placement Status"
)

st.plotly_chart(fig2)

# Package Distribution
fig3 = px.histogram(
    df,
    x="package_lpa",
    title="Package Distribution"
)

st.plotly_chart(fig3)
