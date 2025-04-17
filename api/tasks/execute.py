import json

from api.exceptions import exception_handler
from api.pydantic_models import SQLCommand, ConsultationOutput
from src.agents import executor


def execute(request: ConsultationOutput) -> SQLCommand:
    recommendation = request.recommendation

    try:
        response = executor.run(
            recommendation
        )
    except Exception as e:
        exception_handler(e)

    return response