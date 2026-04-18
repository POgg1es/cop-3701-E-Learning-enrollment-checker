import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

# -----------------------------------
# PAGE SETUP
# -----------------------------------
st.set_page_config(page_title="Student Dashboard", layout="wide")
st.title("Student Course and Assessment Dashboard")

DB_FILE = "student_app.db"
DATA_FOLDER = Path(r"C:\Users\richi\Downloads\Codes\DBMS\data")
SQL_FILE = Path("features.sql")


# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------
@st.cache_resource
def get_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# -----------------------------------
# CREATE TABLES
# -----------------------------------
def create_tables(conn):
    conn.executescript("""
    DROP TABLE IF EXISTS STUDENT_ASSESSMENT;
    DROP TABLE IF EXISTS STUDENT_REGISTRATION;
    DROP TABLE IF EXISTS ASSESSMENT;
    DROP TABLE IF EXISTS COURSE;
    DROP TABLE IF EXISTS STUDENT;

    CREATE TABLE STUDENT (
        id_student INTEGER PRIMARY KEY,
        gender TEXT,
        region TEXT,
        highest_education TEXT,
        imd_band TEXT,
        age_band TEXT,
        final_result TEXT
    );

    CREATE TABLE COURSE (
        code_module TEXT,
        code_presentation TEXT,
        module_presentation_length INTEGER,
        PRIMARY KEY (code_module, code_presentation)
    );

    CREATE TABLE ASSESSMENT (
        id_assessment INTEGER PRIMARY KEY,
        code_module TEXT,
        code_presentation TEXT,
        assessment_type TEXT,
        date TEXT,
        weight REAL,
        FOREIGN KEY (code_module, code_presentation)
            REFERENCES COURSE(code_module, code_presentation)
    );

    CREATE TABLE STUDENT_REGISTRATION (
        id_student INTEGER PRIMARY KEY,
        date_registration TEXT,
        date_unregistration TEXT,
        FOREIGN KEY (id_student)
            REFERENCES STUDENT(id_student)
    );

    CREATE TABLE STUDENT_ASSESSMENT (
        id_student INTEGER,
        id_assessment INTEGER,
        date_submitted TEXT,
        score REAL,
        PRIMARY KEY (id_student, id_assessment),
        FOREIGN KEY (id_student)
            REFERENCES STUDENT(id_student),
        FOREIGN KEY (id_assessment)
            REFERENCES ASSESSMENT(id_assessment)
    );
    """)
    conn.commit()


# -----------------------------------
# LOAD CSV FILES
# -----------------------------------
@st.cache_data
def load_csv_data():
    students = pd.read_csv(DATA_FOLDER / "students.csv")
    courses = pd.read_csv(DATA_FOLDER / "courses.csv")
    assessments = pd.read_csv(DATA_FOLDER / "assessments.csv")
    registrations = pd.read_csv(DATA_FOLDER / "student_registration.csv")
    student_assessment = pd.read_csv(DATA_FOLDER / "student_assessment.csv")

    return students, courses, assessments, registrations, student_assessment


# -----------------------------------
# INSERT DATA INTO DATABASE
# -----------------------------------
def insert_data(conn):
    students, courses, assessments, registrations, student_assessment = load_csv_data()

    students.to_sql("STUDENT", conn, if_exists="append", index=False)
    courses.to_sql("COURSE", conn, if_exists="append", index=False)
    assessments.to_sql("ASSESSMENT", conn, if_exists="append", index=False)
    registrations.to_sql("STUDENT_REGISTRATION", conn, if_exists="append", index=False)
    student_assessment.to_sql("STUDENT_ASSESSMENT", conn, if_exists="append", index=False)

    conn.commit()


# -----------------------------------
# INITIALIZE DATABASE
# -----------------------------------
def initialize_database():
    conn = get_connection()

    try:
        result = pd.read_sql_query("SELECT COUNT(*) AS total FROM STUDENT", conn)
        if result["total"][0] > 0:
            return "Database already loaded."
    except Exception:
        pass

    create_tables(conn)
    insert_data(conn)
    return "Database created and data inserted."


# -----------------------------------
# LOAD QUERIES FROM features.sql
# -----------------------------------
@st.cache_data
def load_queries():
    """
    Reads features.sql and splits queries by semicolon.
    Assumes the file contains exactly 5 queries in this order:
    1. Student Profile
    2. Assessment Results
    3. Performance Dashboard
    4. Leaderboard
    5. Search Page
    """
    sql_text = SQL_FILE.read_text(encoding="utf-8")
    queries = [q.strip() for q in sql_text.split(";") if q.strip()]

    if len(queries) < 5:
        raise ValueError("features.sql must contain at least 5 SQL queries separated by semicolons.")

    return {
        "student_profile": queries[0],
        "assessment_results": queries[1],
        "performance_dashboard": queries[2],
        "leaderboard": queries[3],
        "search_page": queries[4],
    }


# -----------------------------------
# RUN QUERY
# -----------------------------------
@st.cache_data
def run_query(query, params=()):
    conn = get_connection()
    return pd.read_sql_query(query, conn, params=params)


# -----------------------------------
# STARTUP
# -----------------------------------
status = initialize_database()
st.success(status)

queries = load_queries()


# -----------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------
page = st.sidebar.selectbox(
    "Choose a page",
    [
        "Home",
        "Student Profile",
        "Assessment Results",
        "Performance Dashboard",
        "Leaderboard",
        "Search Student"
    ]
)


# -----------------------------------
# HOME PAGE
# -----------------------------------
if page == "Home":
    st.subheader("Home")

    col1, col2, col3 = st.columns(3)

    with col1:
        total_students = run_query("SELECT COUNT(*) AS total FROM STUDENT")
        st.metric("Total Students", int(total_students.iloc[0]["total"]))

    with col2:
        total_courses = run_query("SELECT COUNT(*) AS total FROM COURSE")
        st.metric("Total Courses", int(total_courses.iloc[0]["total"]))

    with col3:
        total_assessments = run_query("SELECT COUNT(*) AS total FROM ASSESSMENT")
        st.metric("Total Assessments", int(total_assessments.iloc[0]["total"]))

    st.subheader("Preview of Students")
    preview = run_query("SELECT * FROM STUDENT LIMIT 10")
    st.dataframe(preview, use_container_width=True)


# -----------------------------------
# STUDENT PROFILE PAGE
# -----------------------------------
elif page == "Student Profile":
    st.subheader("Student Profile")

    student_id = st.number_input("Enter Student ID", min_value=1, step=1, value=1)

    if st.button("Load Student Profile"):
        df = run_query(queries["student_profile"], (student_id,))
        if df.empty:
            st.warning("No student found with that ID.")
        else:
            st.dataframe(df, use_container_width=True)


# -----------------------------------
# ASSESSMENT RESULTS PAGE
# -----------------------------------
elif page == "Assessment Results":
    st.subheader("Assessment Results")

    assessment_id = st.number_input("Enter Assessment ID", min_value=1, step=1, value=1)

    if st.button("Load Assessment Results"):
        df = run_query(queries["assessment_results"], (assessment_id,))
        if df.empty:
            st.warning("No assessment results found for that ID.")
        else:
            st.dataframe(df, use_container_width=True)


# -----------------------------------
# PERFORMANCE DASHBOARD PAGE
# -----------------------------------
elif page == "Performance Dashboard":
    st.subheader("Student Performance Dashboard")

    df = run_query(queries["performance_dashboard"])
    st.dataframe(df, use_container_width=True)


# -----------------------------------
# LEADERBOARD PAGE
# -----------------------------------
elif page == "Leaderboard":
    st.subheader("Top Students Leaderboard")

    df = run_query(queries["leaderboard"])
    st.dataframe(df, use_container_width=True)


# -----------------------------------
# SEARCH PAGE
# -----------------------------------
elif page == "Search Student":
    st.subheader("Search Student")

    search_id = st.text_input("Search by Student ID", placeholder="Example: 12")

    if st.button("Search"):
        if not search_id.strip().isdigit():
            st.error("Please enter a valid numeric student ID.")
        else:
            student_id = int(search_id.strip())
            df = run_query(queries["search_page"], (student_id,))
            if df.empty:
                st.warning("No student found.")
            else:
                st.dataframe(df, use_container_width=True)