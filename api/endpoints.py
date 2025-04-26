from fastapi import APIRouter, HTTPException
from api.pydantic_models import Query, Answer
from api.tasks.answer import answer
import logging


logger = logging.getLogger("uvicorn.error")

router = APIRouter(prefix="/v1") 

# answer endpoint
@router.post("/answer", response_model=Answer)
async def answer_endpoint(request: Query) -> Answer:
	"""
	Answers a query.
	"""
	try:
		result = answer(request.query)
		return result
	except Exception as e:
		logger.exception("Answer failed")
		raise HTTPException(status_code=500, detail=str(e))

# test endpoint
@router.get("/test")
async def test_endpoint():
	return {"message": "Hello, World!"}

