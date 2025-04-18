from api import app
from api.pydantic_models import ConsultationOutput, BusinessData, SQLCommand
from api.tasks.execute import execute
from api.tasks.consulte import consulte


# chat endpoint
@app.post("/consulte")
async def consulting(
	request: BusinessData,
):
	response = consulte(
		request,
	)

	return ConsultationOutput(recommendations=response.recommendations)


# scheduling endpoint
@app.post("/execute")
async def executing(
	request: ConsultationOutput
):
	response = execute(
		request,
	)

	return SQLCommand()