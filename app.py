import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------
# Load Dataset
# ------------------------------

df = pd.read_csv("placements.csv")

# ------------------------------
# Session State
# ------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "student" not in st.session_state:
    st.session_state.student = None

# ------------------------------
# LOGIN PAGE
# ------------------------------

if not st.session_state.logged_in:

    st.title("🎓 College Placement Analytics System")

    login_type = st.selectbox(
        "Login As",
        ["Student", "Admin"]
    )

    # --------------------------
    # Student Login
    # --------------------------

    if login_type == "Student":

        roll_no = st.text_input("Roll Number")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Student Login"):

            student = df[
                (df["roll_no"].astype(str) == roll_no)
                &
                (df["password"].astype(str) == password)
            ]

            if len(student) > 0:

                st.session_state.logged_in = True
                st.session_state.role = "student"
                st.session_state.student = student.iloc[0]

                st.rerun()

            else:
                st.error("Invalid Credentials")

    # --------------------------
    # Admin Login
    # --------------------------

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

# ------------------------------
# Sidebar
# ------------------------------

st.sidebar.title("Navigation")

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.student = None

    st.rerun()

# ======================================================
# STUDENT DASHBOARD
# ======================================================

if st.session_state.role == "student":

    student = st.session_state.student

    st.title("🎓 Student Dashboard")

    st.subheader("Student Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Name:", student["student_name"])
        st.write("### Roll No:", student["roll_no"])
        st.write("### Department:", student["department"])

    with col2:
        st.write("### CGPA:", student["cgpa"])
        st.write("### Company:", student["company_name"])
        st.write("### Package:", student["package_lpa"], "LPA")

    st.markdown("---")

    # CGPA Gauge

    st.subheader("CGPA Performance")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=float(student["cgpa"]),
        title={'text': "CGPA"},
        gauge={
            'axis': {'range': [0, 10]}
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    # Student vs Average

    st.subheader("Student vs College Average")

    avg_cgpa = df["cgpa"].mean()

    compare_df = pd.DataFrame({
        "Category": [
            "Student CGPA",
            "College Average"
        ],
        "CGPA": [
            student["cgpa"],
            avg_cgpa
        ]
    })

    fig = px.bar(
        compare_df,
        x="Category",
        y="CGPA",
        title="CGPA Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Placement Status Pie Chart

    st.subheader("Placement Statistics")

    status = (
        df["placement_status"]
        .value_counts()
        .reset_index()
    )

    status.columns = [
        "Status",
        "Count"
    ]

    fig = px.pie(
        status,
        names="Status",
        values="Count",
        title="Placed vs Not Placed"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Department Average Package

    st.subheader("Department Average Package")

    dept_package = (
        df.groupby("department")["package_lpa"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        dept_package,
        x="department",
        y="package_lpa",
        title="Average Package by Department"
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# ADMIN DASHBOARD
# ======================================================

if st.session_state.role == "admin":

    st.title("📊 Admin Dashboard")

    total_students = len(df)

    placed_students = len(
        df[
            df["placement_status"] == "Placed"
        ]
    )

    placement_percentage = round(
        (placed_students / total_students) * 100,
        2
    )

    avg_package = round(
        df["package_lpa"].mean(),
        2
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Students",
        total_students
    )

    col2.metric(
        "Placed Students",
        placed_students
    )

    col3.metric(
        "Placement %",
        placement_percentage
    )

    col4.metric(
        "Avg Package",
        avg_package
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
            .astype(str)
            .str.contains(search)
        ]

        st.dataframe(result)

    # Department Filter

    st.subheader("Department Filter")

    dept = st.selectbox(
        "Select Department",
        ["All"] +
        list(df["department"].unique())
    )

    if dept == "All":
        filtered = df
    else:
        filtered = df[
            df["department"] == dept
        ]

    st.dataframe(filtered)

    # Download Report

    csv = filtered.to_csv(
        index=False
    )

    st.download_button(
        "Download Report",
        csv,
        "placement_report.csv",
        "text/csv"
    )

    st.markdown("---")

    # Department-wise Students

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

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # Placement Pie Chart

    status = (
        df["placement_status"]
        .value_counts()
        .reset_index()
    )

    status.columns = [
        "Status",
        "Count"
    ]

    fig2 = px.pie(
        status,
        names="Status",
        values="Count",
        title="Placement Status"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # Top Recruiters

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

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # Highest Package

    st.subheader("Highest Package Student")

    highest = df.loc[
        df["package_lpa"].idxmax()
    ]

    st.success(
        f"{highest['student_name']} "
        f"got {highest['package_lpa']} LPA "
        f"in {highest['company_name']}"
    )
