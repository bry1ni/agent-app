from agno.agent import Agent

from src.config.prompts import EXECUTOR_INSTRUCTION
from src.models.sql_command import SQLCommand
# from src.tools.executor import send_and_execute_sql_command
from src.agents import gpt
from typing import List

executor = Agent(
	name="executor",
	model=gpt,
	instructions=EXECUTOR_INSTRUCTION,
	response_model=SQLCommand,
    structured_outputs=True
)