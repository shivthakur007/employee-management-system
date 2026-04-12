import streamlit as st
from db import conn, cursor
import mysql.connector


st.title("Employee Management System")

menu = ["Add", "View", "Update", "Delete"]
choice = st.sidebar.selectbox("Menu", menu)

if st.button("Add Employee"):
    try:
        insert_query = """
        INSERT INTO employees 
        (first_name, last_name, email)
        VALUES (%s, %s, %s)
        """

        values = (first_name, last_name, email)

        cursor.execute(insert_query, values)
        conn.commit()

        emp_id = cursor.lastrowid
        emp_code = f"S22{str(emp_id).zfill(5)}"

        cursor.execute(
            "UPDATE employees SET emp_code=%s WHERE employee_id=%s",
            (emp_code, emp_id)
        )
        conn.commit()

        st.success(f"Employee Added: {emp_code}")

    except Exception:
        st.error("⚠️ Email already exists or error occurred")
        
elif choice == "View":
    st.subheader("Employee List")

    cursor.execute("SELECT employee_id, emp_code, first_name, last_name, salary FROM employees")
    data = cursor.fetchall()

    st.write(data)

elif choice == "Update":
    st.subheader("Update Employee Salary")

    emp_id = st.number_input("Enter Employee ID", min_value=1)
    new_salary = st.number_input("New Salary", min_value=0.0)

    if st.button("Update"):
        query = "UPDATE employees SET salary=%s WHERE employee_id=%s"
        cursor.execute(query, (new_salary, emp_id))
        conn.commit()

        st.success("Employee updated successfully")

elif choice == "Delete":
    st.subheader("Delete Employee")

    emp_id = st.number_input("Enter Employee ID to delete", min_value=1)

    if st.button("Delete"):
        cursor.execute("DELETE FROM employees WHERE employee_id=%s", (emp_id,))
        conn.commit()

        st.warning("Employee deleted successfully")