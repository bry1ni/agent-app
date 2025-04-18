from agno.tools import tool
from typing import Dict, Any
from src.tasks.executing.execute import execute_sql_command
from src.tools.utils import send as send_email


@tool
def send_and_execute_sql_command(sql_command: str) -> Dict[str, Any]:
    """
    Sends a SQL command to the database and returns execution results.

    This tool wraps the `execute_sql_command` function and allows execution of 
    raw SQL commands on a PostgreSQL database. It can handle SELECTs, DML operations, 
    and optionally log pre/post-checks (if enabled in the internal implementation).

    Parameters:
        sql_command (str): The SQL command to be executed. 
            Example: "SELECT * FROM users WHERE is_active = TRUE;"

    Returns:
        Dict[str, Any]: A dictionary containing the execution outcome, such as:
            - success (bool): Whether the command executed successfully.
            - main_result (Any): Result of the main SQL query (e.g., rows for SELECT).
            - pre_checks (dict): Results of any pre-check queries.
            - post_checks (dict): Results of any post-check queries.
            - rows_affected (int): Number of rows affected for DML queries.
            - error (str | None): Error message, if any.
    """
    return execute_sql_command(sql_command)


@tool
def email_user(to: str, subject: str, body: str) -> Dict[str, Any]:
    """
    Sends an email to a user with the specified subject and body.
    
    Args:
        to (str): The recipient's email address
        subject (str): The email subject
        body (str): The email body content
        
    Returns:
        Dict[str, Any]: A dictionary containing the email sending status
    """
    try:
        # For now, we'll use a dummy first_name and empty lists for insights and recs
        # since the current send function requires these parameters
        send_email(
            to=to,
            first_name="User",
            insight_table=[],
            recs=[],
            dashboard_url="",
            tasks_line=body
        )
        return {"success": True, "message": "Email sent successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)} 