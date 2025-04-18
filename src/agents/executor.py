from agno.agent import Agent
from agno.tools.email import EmailTools

from src.config.prompts import EXECUTOR_INSTRUCTION
from src.models.sql_command import SQLCommand
# from src.tools.executor import send_and_execute_sql_command
from src.agents import gpt
from typing import List
from src.tools.executor import email_user

executor = Agent(
	name="executor",
	model=gpt,
	instructions=EXECUTOR_INSTRUCTION,
	response_model=SQLCommand,
    tools=[email_user],
    structured_outputs=True
)