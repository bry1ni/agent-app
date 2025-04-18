from typing import Dict, List, Any, Optional, Union

from src.tasks.executing import conn, cursor

def execute_sql_command(sql: str, 
                        pre_checks: Optional[List[str]] = None,
                        post_checks: Optional[List[str]] = None,
                        use_transaction: bool = True,
                        conn=conn,
                        cursor=cursor) -> Dict[str, Any]:
    """
    Execute a SQL command in PostgreSQL with optional pre and post check queries.
    
    Args:
        sql: The SQL command to execute
        connection_params: Dictionary containing database connection parameters
                         (dbname, user, password, host, port)
        pre_checks: Optional list of SQL queries to run before the main command
        post_checks: Optional list of SQL queries to run after the main command
        use_transaction: Whether to wrap the execution in a transaction
        
    Returns:
        Dictionary containing execution results and any pre/post check results
    """
    results = {
        "success": False,
        "main_result": None,
        "pre_checks": {},
        "post_checks": {},
        "rows_affected": 0,
        "error": None
    }
    
    conn = None
    try:
        if use_transaction:
            conn.autocommit = False
        else:
            conn.autocommit = True
        
        if pre_checks:
            for i, check_sql in enumerate(pre_checks):
                cursor.execute(check_sql)
                results["pre_checks"][f"check_{i+1}"] = cursor.fetchall()
        
        cursor.execute(sql) # execute sql command
        
        # Get results if it's a SELECT query
        if sql.strip().upper().startswith("SELECT"):
            results["main_result"] = cursor.fetchall()
        else:
            results["rows_affected"] = cursor.rowcount
        
        if post_checks:
            for i, check_sql in enumerate(post_checks):
                cursor.execute(check_sql)
                results["post_checks"][f"check_{i+1}"] = cursor.fetchall()
        
        if use_transaction:
            conn.commit()
        
        results["success"] = True
        
    except Exception as e:
        # roll back transaction on error if we're using one
        if conn and use_transaction and not conn.closed:
            conn.rollback()
        results["error"] = str(e)
        
    finally:
        if conn and not conn.closed:
            conn.close()
            
    return results