import json
from typing import Dict, Any, List
from src.agents.utils import extract_response_from_agent
from api.exceptions import exception_handler
from api.pydantic_models import ConsultationOutput
from src.models.sql_command import SQLCommand
from src.agents.executor import executor


def execute(request: ConsultationOutput) -> List[SQLCommand]:
    recommendations = request.recommendations
    
    try:
        all_sql = []
        for recommendation in recommendations:
            
            response = executor.run(
                recommendation
            )
            result = extract_response_from_agent(response, "executor")
            all_sql.append(SQLCommand(sql=result["sql"]))

        # Join all SQL commands with newlines
        return all_sql
    except Exception as e:
        exception_handler(e)
        raise