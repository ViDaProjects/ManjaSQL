query = """
INSERT INTO employees (emp_no, birth_date, first_name, last_name, gender, hire_date)
VALUES (101, '2000-01-01', 'John', 'Doe', 'M', '2023-01-01');

UPDATE employees
SET first_name = 'Jane', last_name = 'Smith'
WHERE emp_no = 101;

DELETE FROM employees
WHERE emp_no = 101;

SELECT emp_no, MAX(from_date) AS from_date, MAX(to_date) AS to_date
    FROM dept_emp
    GROUP BY emp_no;
"""

query_lower = query.lower()

query_lower = query_lower.replace("insert into", "colocar")
query_lower = query_lower.replace("update", "modificar")
query_lower = query_lower.replace("delete from", "apagar")
query_lower = query_lower.replace("select", "agarrar")

print(query_lower)
