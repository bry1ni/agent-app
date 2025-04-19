from fastapi import APIRouter, HTTPException, BackgroundTasks
from api.pydantic_models import BusinessData, ConsultationOutput
from api.tasks.consulte import consulte
from api.tasks.execute import execute
import logging
from src.tools.utils import send as send_mail
import json
from typing import List
from src.models.sql_command import SQLCommand


logger = logging.getLogger("uvicorn.error")

router = APIRouter(prefix="/v1") 
OWNER_EMAIL = "r.benatallah01@gmail.com" 

# consultation endpoint
@router.post("/consult", response_model=ConsultationOutput)
async def consult_endpoint(
	request: BusinessData,
	background_tasks: BackgroundTasks
):
	"""
     Handles business consultation requests.
     Sends email in the background once consultation is complete.
	"""
	try:
		result = await consulte(request)
		background_tasks.add_task(
			send_mail,
			OWNER_EMAIL,                  
			"Dina", 
			[("Weekly summary", result.summary_report)],  
			result.recommendations,       
			"https://dashboard.ayorservices.com"
		)

		return result
	except Exception as e:
		logger.exception("Consultation failed")
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

