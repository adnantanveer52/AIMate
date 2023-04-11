import pandas as pd
import streamlit as st
import pymysql
from flask import jsonify, request
import datetime
import requests


connection = pymysql.connect(host='localhost', user='root', password='', db='pm')
cursor = connection.cursor()


  # Flask Code

def fetch_projects():
    response = cursor.execute("SELECT * from projects")
    projects = response.json()
    return pd.DataFrame(projects, columns=["id", "name", "description", "start_date", "end_date", "status"])

def add_project():
    data = request.get_json()
    name = data.get('name', '')
    description = data.get('description', '')
    start_date = data.get('start_date', datetime.datetime.now())
    end_date = data.get('end_date', '')
    status = data.get('status', 'Not Started')

    cursor.execute(
        "INSERT INTO projects (name, description, start_date, end_date, status) VALUES (%s, %s, %s, %s, %s)",
        (name, description, start_date, end_date, status))
    connection.commit()
    cursor.close()

    return jsonify({"message": "Project added successfully"})

def project_dashboard1():
    st.header("Project Dashboard")

    # Add project form
    with st.form(key="add_project_form"):
        name = st.text_input("Project Name")
        description = st.text_area("Project Description")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date", value=None)
        status = st.selectbox("Status", ["Not Started", "In Progress", "Completed", "On Hold"])

        submit_button = st.form_submit_button(label="Add Project")
        if submit_button:
            response = add_project(name, description, start_date, end_date, status)
            st.success(response["message"])
    # Show projects
    projects = fetch_projects()
    st.write(projects)










def main():
    if "page" not in st.session_state:
        st.session_state.page = 0

    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose a functionality", ["Project Dashboard", "Task Management", "Time Tracking", "Team Collaboration", "Reporting", "Budgeting", "Communication", "Proofing & Feedback"])
    if app_mode == "Project Dashboard":
        project_dashboard()
    elif app_mode == "Task Management":
        task_management()
    elif app_mode == "Time Tracking":
        time_tracking()
    elif app_mode == "Team Collaboration":
        team_collaboration()
    elif app_mode == "Reporting":
        reporting()
    elif app_mode == "Budgeting":
        budgeting()
    elif app_mode == "Communication":
        communication()
    elif app_mode == "Proofing & Feedback":
        proofing_feedback()

def project_dashboard():
    st.header("Project Dashboard")
    project_dashboard1()
    if st.button("Add Project"):
        add_project()
def task_management():
    st.header("Task Management")

def time_tracking():
    st.header("Time Tracking")

def team_collaboration():
    st.header("Team Collaboration")

def reporting():
    st.header("Reporting")

def budgeting():
    st.header("Budgeting")

def communication():
    st.header("Communication")

def proofing_feedback():
    st.header("Proofing & Feedback")

if __name__ == "__main__":
    main()
