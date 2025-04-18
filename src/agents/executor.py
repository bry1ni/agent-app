from agno.agent import Agent
from agno.tools.thinking import ThinkingTools

from src.config.prompts import EXECUTOR_INSTRUCTION
from api.pydantic_models import SQLCommand
from src.tools.executor import send_and_execute_sql_command
from src.agents import gpt


executor = Agent(
	name="executor",
	model=gpt,
	instructions=EXECUTOR_INSTRUCTION,
	tools=[ThinkingTools(), send_and_execute_sql_command],
	response_model=SQLCommand
)