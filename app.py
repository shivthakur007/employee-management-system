from db import conn, cursor

def add_employee():
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    hire_date = input("Hire Date (YYYY-MM-DD): ")
    salary = float(input("Salary: "))
    department_id = int(input("Department ID: "))
    job_id = int(input("Job ID: "))
    manager_id = input("Manager ID (or press enter): ")
    location = input("Location: ")

    manager_id = int(manager_id) if manager_id else None

    query = """
    INSERT INTO employees 
    (first_name, last_name, email, phone, hire_date, salary, department_id, job_id, manager_id, joining_location)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (first_name, last_name, email, phone, hire_date, salary, department_id, job_id, manager_id, location)

    cursor.execute(query, values)
    conn.commit()

    emp_id = cursor.lastrowid
    emp_code = f"S22{str(emp_id).zfill(5)}"

    cursor.execute("UPDATE employees SET emp_code=%s WHERE employee_id=%s", (emp_code, emp_id))
    conn.commit()

    print("Employee Added:", emp_code)

def view_employees():
    cursor.execute("SELECT employee_id, emp_code, first_name, last_name, salary FROM employees")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def update_employee():
    emp_id = int(input("Enter Employee ID to update: "))
    new_salary = float(input("Enter new salary: "))

    query = "UPDATE employees SET salary = %s WHERE employee_id = %s"
    cursor.execute(query, (new_salary, emp_id))
    conn.commit()

    print("Employee updated!")

def delete_employee():
    emp_id = int(input("Enter Employee ID to delete: "))

    cursor.execute("DELETE FROM employees WHERE employee_id = %s", (emp_id,))
    conn.commit()

    print("Employee deleted!")

def main():
    while True:
        print("\n1. Add Employee")
        print("2. View Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_employee()
        elif choice == "2":
            view_employees()
        elif choice == "3":
            update_employee()
        elif choice == "4":
            delete_employee()
        elif choice == "5":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
    