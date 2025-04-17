from agno.agent import Agent

from src.config.prompts import EXECUTOR_INSTRUCTION
from api.pydantic_models import SQLCommand
from src.agents import gpt


executor = Agent(
	name="executor",
	model=gpt,
	instructions=EXECUTOR_INSTRUCTION,
	tools=[],
	response_model=SQLCommand
)