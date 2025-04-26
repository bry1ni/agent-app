from agno.agent import Agent

from src.config.prompts import AGENT_INSTRUCTION
from src.agents import gpt
from api.pydantic_models import Answer
from src.tools.agent import tool_name


agent = Agent(
	name="agent",
	model=gpt,
	instructions=AGENT_INSTRUCTION,
	response_model=Answer,
    tools=[tool_name],
    structured_outputs=True
)