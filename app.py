import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
df = pd.read_csv("placements.csv")

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "student" not in st.session_state:
    st.session_state.student = None

# LOGIN PAGE
if not st.session_state.logged_in:

    st.title("🎓 College Placement Analytics System")

    login_type = st.selectbox(
        "Login As",
        ["Student", "Admin"]
    )

    # STUDENT LOGIN
    if login_type == "Student":

        roll_no = st.text_input("Roll Number")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Student Login"):

            student = df[
                (df["roll_no"] == roll_no)
                & (df["password"].astype(str) == password)
            ]

            if len(student) > 0:

                st.session_state.logged_in = True
                st.session_state.role = "student"
                st.session_state.student = student.iloc[0]

                st.rerun()

            else:
                st.error("Invalid Credentials")

    # ADMIN LOGIN
    else:

        username = st.text_input("Admin Username")

        password = st.text_input(
            "Admin Password",
            type="password"
        )

        if st.button("Admin Login"):

            if username == "admin" and password == "admin123":

                st.session_state.logged_in = True
                st.session_state.role = "admin"

                st.rerun()

            else:
                st.error("Invalid Admin Credentials")

    st.stop()

# LOGOUT
st.sidebar.success("Logged In")

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.student = None

    st.rerun()

# STUDENT DASHBOARD
if st.session_state.role == "student":

    student = st.session_state.student

    st.title("🎓 Student Dashboard")

    st.subheader("Student Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Name:", student["student_name"])
        st.write("Roll No:", student["roll_no"])
        st.write("Department:", student["department"])

    with col2:
        st.write("CGPA:", student["cgpa"])
        st.write("Company:", student["company_name"])
        st.write("Package:", student["package_lpa"])

# ADMIN DASHBOARD
if st.session_state.role == "admin":

    st.title("📊 Admin Dashboard")

    # KPIs
    total_students = len(df)

    placed_students = len(
        df[df["placement_status"] == "Placed"]
    )

    placement_percentage = round(
        placed_students / total_students * 100,
        2
    )

    avg_package = round(
        df["package_lpa"].mean(),
        2
    )

    highest_package = df["package_lpa"].max()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Students", total_students)

    c2.metric(
        "Placed Students",
        placed_students
    )

    c3.metric(
        "Placement %",
        f"{placement_percentage}%"
    )

    c4.metric(
        "Highest Package",
        highest_package
    )

    st.markdown("---")

    # Search Student
    st.subheader("Search Student")

    search = st.text_input(
        "Enter Roll Number"
    )

    if search:

        result = df[
            df["roll_no"]
            .str.contains(search, case=False)
        ]

        st.dataframe(result)

    # Department Filter
    st.subheader("Department Filter")

    dept = st.selectbox(
        "Department",
        ["All"] +
        list(df["department"].unique())
    )

    if dept != "All":

        filtered = df[
            df["department"] == dept
        ]

    else:

        filtered = df

    st.dataframe(filtered)

    # Download Report
    csv = filtered.to_csv(index=False)

    st.download_button(
        "Download Report",
        csv,
        "placement_report.csv",
        "text/csv"
    )

    st.markdown("---")

    # Department-wise Chart
    dept_chart = (
        df.groupby("department")
        .size()
        .reset_index(name="count")
    )

    fig1 = px.bar(
        dept_chart,
        x="department",
        y="count",
        title="Department-wise Students"
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

    # Company-wise Hiring
    company = (
        df.groupby("company_name")
        .size()
        .reset_index(name="count")
    )

    fig3 = px.bar(
        company,
        x="company_name",
        y="count",
        title="Top Recruiters"
    )

    st.plotly_chart(fig3)
