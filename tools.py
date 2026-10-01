# tools.py

# This function simulates looking up an employee's information.
def get_employee_info(employee_id):
    # In a real application, this information would come from
    # a database, HR system, or an API.
    employees = {
        "EMP001": {
            "name": "John",
            "department": "Data Science",
            "role": "Data Scientist"
        },
        "EMP002": {
            "name": "Sarah",
            "department": "Human Resources",
            "role": "HR Manager"
        }
    }

    # Look for the employee ID in our fake employee database.
    employee = employees.get(employee_id)

    # If the employee doesn't exist, return an appropriate message.
    if employee is None:
        return f"Employee {employee_id} was not found."

    # Return the employee information.
    return employee


# This function simulates checking an employee's leave balance.
def check_leave_balance(employee_id):
    # Fake leave balances for demonstration purposes.
    leave_balances = {
        "EMP001": 12,
        "EMP002": 18
    }

    # Look up the employee's leave balance.
    balance = leave_balances.get(employee_id)

    # If the employee doesn't exist, return an appropriate message.
    if balance is None:
        return f"Employee {employee_id} was not found."

    # Return the number of remaining leave days.
    return f"{employee_id} has {balance} days of leave remaining."


# This function simulates creating an IT support ticket.
def create_it_ticket(employee_id, issue):
    # In a real application, this would create a ticket
    # in something like ServiceNow, Jira, or another IT system.

    # For now, we simply return a fake ticket ID.
    ticket_id = "IT-1001"

    return (
        f"IT ticket {ticket_id} created for {employee_id}. "
        f"Issue: {issue}"
    )