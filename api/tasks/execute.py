import json

from api.exceptions import exception_handler
from api.pydantic_models import SQLCommand, ConsultationOutput
from src.agents.executor import executor


def execute(request: ConsultationOutput) -> SQLCommand:
    recommendation = request.recommendations

    try:
        response = executor.run(
            recommendation
        )
    except Exception as e:
        exception_handler(e)

    return response