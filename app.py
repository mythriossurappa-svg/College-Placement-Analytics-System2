import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="College Placement Analytics", layout="wide")

try:
    df = pd.read_csv("placements.csv")
except Exception:
    st.error("Could not load data/placements.csv")
    st.stop()

st.title("College Placement Analytics System")

total_students = len(df)
placed = (df["placement_status"]=="Placed").sum()
placement_pct = round((placed/total_students)*100,2)
avg_package = round(df["package_lpa"].mean(),2)

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Students", total_students)
c2.metric("Placed Students", placed)
c3.metric("Placement %", placement_pct)
c4.metric("Avg Package (LPA)", avg_package)

st.subheader("Placement Data")
st.dataframe(df)

dept = df.groupby("department").size().reset_index(name="count")
fig1 = px.bar(dept, x="department", y="count", title="Department-wise Placements")
st.plotly_chart(fig1, use_container_width=True)

company = df.groupby("company_name").size().reset_index(name="count")
fig2 = px.pie(company, names="company_name", values="count", title="Company-wise Hiring")
st.plotly_chart(fig2, use_container_width=True)

yearly = df.groupby("placement_year").size().reset_index(name="count")
fig3 = px.line(yearly, x="placement_year", y="count", markers=True, title="Placement Trend")
st.plotly_chart(fig3, use_container_width=True)
