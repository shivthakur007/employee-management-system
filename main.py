from db import conn, cursor

# Insert employee (without emp_code)
insert_query = """
INSERT INTO employees 
(first_name, last_name, email, phone, hire_date, salary, department_id, job_id, manager_id, joining_location)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

values = (
    "Rahul",
    "Sharma",
    "rahul@gmail.com",
    "9999999999",
    "2025-04-01",
    30000,
    1,
    2,
    None,
    "Mumbai"
)

cursor.execute(insert_query, values)
conn.commit()

# Get last inserted ID
emp_id = cursor.lastrowid

# Generate emp_code
emp_code = f"S22{str(emp_id).zfill(5)}"

# Update emp_code
update_query = "UPDATE employees SET emp_code = %s WHERE employee_id = %s"
cursor.execute(update_query, (emp_code, emp_id))
conn.commit()

print("Employee inserted with code:", emp_code)