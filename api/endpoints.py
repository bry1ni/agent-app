from fastapi import APIRouter, HTTPException, BackgroundTasks
from api.pydantic_models import BusinessData, ConsultationOutput, StoreAnalyticsSchema
from api.tasks.consulte import consulte
from api.tasks.execute import execute
import logging
from src.tools.utils import send as send_mail
import json
from typing import List, Optional, Union
from src.models.sql_command import SQLCommand
from src.tasks.consulting.consulte import get_complete_analytics
from src.tasks.utils import get_token


logger = logging.getLogger("uvicorn.error")

router = APIRouter(prefix="/v1") 

# consultation endpoint
@router.get("/consult", response_model=ConsultationOutput)
async def analytics_endpoint(
    background_tasks: BackgroundTasks,
    token: Optional[str] = None,
    period: Optional[Union[str, int]] = "week",
    user_email: Optional[str] = None,
    user_name: Optional[str] = None,
    send_report: bool = False,
):
    """
    Handles business analytics requests.
    Optionally sends email report in the background.
    
    Args:
        background_tasks: FastAPI background tasks
        token: Authentication token (optional)
        period: Time period for analysis ("week", "month", or number of days)
        user_email: Email address to send report to (if send_report is True)
        user_name: Name of user to send report to (if send_report is True)
        send_report: Whether to send an email report
    """
    try:
        # Get token if not provided
        auth_token = get_token()
        analytics_data = get_complete_analytics(token=auth_token, period=period)
        result = await consulte(analytics_data)
        return result
    except Exception as e:
        logger.exception("Analytics endpoint failed")
        raise HTTPException(status_code=500, detail=str(e))


# execution endpoint
@router.post("/execute", response_model=List[SQLCommand])
async def execute_endpoint(request: ConsultationOutput):
	"""
	Executes follow-up actions based on consultation result.
	"""
	try:
		result = execute(request)
		return result
	except Exception as e:
		logger.exception("Execution failed")
		raise HTTPException(status_code=500, detail=str(e))

# test endpoint
@router.get("/test")
async def test_endpoint():
	return {"message": "Hello, World!"}

