from agno.agent import Agent

from src.config.prompts import CONSULTANT_INSTRUCTION
from src.agents import gpt
from api.pydantic_models import ConsultationOutput

consultant = Agent(
	name="consultant",
	model=gpt,
	instructions=CONSULTANT_INSTRUCTION,
	tools=[],
	response_model=ConsultationOutput
)