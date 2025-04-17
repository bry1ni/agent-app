import json

from api.exceptions import exception_handler
from api.pydantic_models import BusinessData, ConsultationOutput
from src.agents import consultant


def consulte(request: BusinessData) -> ConsultationOutput:
    business_data = request.business_data

    try:
        response = consultant.run(
            business_data
        )
    except Exception as e:
        exception_handler(e)

    return response