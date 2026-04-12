import streamlit as st
from db import conn, cursor

st.title("Employee Management System")

menu = ["Add Employee", "View Employees", "Update Employee", "Delete Employee"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- ADD EMPLOYEE ----------------
if choice == "Add Employee":
    st.subheader("Add New Employee")

    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    hire_date = st.date_input("Hire Date")
    salary = st.number_input("Salary", min_value=0.0)
    department_id = st.number_input("Department ID", min_value=1)
    job_id = st.number_input("Job ID", min_value=1)
    manager_id = st.text_input("Manager ID (optional)")
    location = st.text_input("Location")

    if st.button("Add Employee"):
        manager_id = int(manager_id) if manager_id else None

        query = """
        INSERT INTO employees 
        (first_name, last_name, email, phone, hire_date, salary, department_id, job_id, manager_id, joining_location)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            first_name, last_name, email, phone, hire_date,
            salary, department_id, job_id, manager_id, location
        )

        cursor.execute(query, values)
        conn.commit()

        emp_id = cursor.lastrowid
        emp_code = f"S22{str(emp_id).zfill(5)}"

        cursor.execute(
            "UPDATE employees SET emp_code=%s WHERE employee_id=%s",
            (emp_code, emp_id)
        )
        conn.commit()

        st.success(f"Employee Added! Code: {emp_code}")

# ---------------- VIEW EMPLOYEES ----------------
elif choice == "View Employees":
    st.subheader("Employee List")

    cursor.execute("""
        SELECT employee_id, emp_code, first_name, last_name, salary 
        FROM employees
    """)

    rows = cursor.fetchall()

    if rows:
        st.table(rows)
    else:
        st.warning("No employees found")

# ---------------- UPDATE EMPLOYEE ----------------
elif choice == "Update Employee":
    st.subheader("Update Employee")

    emp_id = st.number_input("Employee ID", min_value=1)

    option = st.selectbox("Update Field", ["Salary", "Email", "Phone"])

    if option == "Salary":
        new_value = st.number_input("New Salary", min_value=0.0)
    else:
        new_value = st.text_input("New Value")

    if st.button("Update"):
        if option == "Salary":
            cursor.execute(
                "UPDATE employees SET salary=%s WHERE employee_id=%s",
                (new_value, emp_id)
            )
        elif option == "Email":
            cursor.execute(
                "UPDATE employees SET email=%s WHERE employee_id=%s",
                (new_value, emp_id)
            )
        elif option == "Phone":
            cursor.execute(
                "UPDATE employees SET phone=%s WHERE employee_id=%s",
                (new_value, emp_id)
            )

        conn.commit()
        st.success("Employee Updated!")

# ---------------- DELETE EMPLOYEE ----------------
elif choice == "Delete Employee":
    st.subheader("Delete Employee")

    emp_id = st.number_input("Employee ID", min_value=1)

    if st.button("Delete"):
        cursor.execute(
            "DELETE FROM employees WHERE employee_id=%s",
            (emp_id,)
        )
        conn.commit()

        st.success("Employee Deleted!")