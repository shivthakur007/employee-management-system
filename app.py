from db import conn, cursor

def add_employee():
    try:
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        email = input("Email: ").strip()
        phone = input("Phone: ").strip()
        hire_date = input("Hire Date (YYYY-MM-DD): ").strip()
        salary = float(input("Salary: "))
        department_id = int(input("Department ID: "))
        job_id = int(input("Job ID: "))
        manager_id = input("Manager ID (press enter if none): ").strip()
        location = input("Location: ").strip()

        manager_id = int(manager_id) if manager_id else None

        query = """
        INSERT INTO employees 
        (first_name, last_name, email, phone, hire_date, salary, department_id, job_id, manager_id, joining_location)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (first_name, last_name, email, phone, hire_date, salary,
                  department_id, job_id, manager_id, location)

        cursor.execute(query, values)
        conn.commit()

        # Generate emp_code
        emp_id = cursor.lastrowid
        emp_code = f"S22{str(emp_id).zfill(5)}"

        cursor.execute(
            "UPDATE employees SET emp_code=%s WHERE employee_id=%s",
            (emp_code, emp_id)
        )
        conn.commit()

        print(f"✅ Employee Added Successfully! Code: {emp_code}")

    except Exception as e:
        print("❌ Error:", e)

def view_employees():
    cursor.execute("""
        SELECT employee_id, emp_code, first_name, last_name, salary 
        FROM employees
    """)

    rows = cursor.fetchall()

    if not rows:
        print("⚠️ No employees found")
        return

    print("\n--- Employee List ---")
    print("ID | Code | Name | Salary")
    print("-" * 40)

    for row in rows:
        emp_id, code, fname, lname, salary = row
        print(f"{emp_id} | {code} | {fname} {lname} | {salary}")


def update_employee():
    try:
        emp_id = int(input("Enter Employee ID to update: "))

        print("\nWhat do you want to update?")
        print("1. Salary")
        print("2. Email")
        print("3. Phone")

        choice = input("Enter choice: ")

        if choice == "1":
            new_salary = float(input("Enter new salary: "))
            cursor.execute(
                "UPDATE employees SET salary = %s WHERE employee_id = %s",
                (new_salary, emp_id)
            )

        elif choice == "2":
            new_email = input("Enter new email: ")
            cursor.execute(
                "UPDATE employees SET email = %s WHERE employee_id = %s",
                (new_email, emp_id)
            )

        elif choice == "3":
            new_phone = input("Enter new phone: ")
            cursor.execute(
                "UPDATE employees SET phone = %s WHERE employee_id = %s",
                (new_phone, emp_id)
            )

        else:
            print("Invalid choice")
            return

        conn.commit()
        print("✅ Employee updated successfully!")

    except Exception as e:
        print("❌ Error:", e)

def delete_employee():
    try:
        emp_id = int(input("Enter Employee ID to delete: "))

        confirm = input("Are you sure? (y/n): ").lower()

        if confirm == 'y':
            cursor.execute(
                "DELETE FROM employees WHERE employee_id = %s",
                (emp_id,)
            )
            conn.commit()
            print("✅ Employee deleted!")
        else:
            print("❌ Deletion cancelled")

    except Exception as e:
        print("❌ Error:", e)