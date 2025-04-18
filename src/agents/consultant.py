from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

from src.config.prompts import CONSULTANT_INSTRUCTION
from src.agents import gpt
from api.pydantic_models import ConsultationOutput
from src.tools.consultant import competitor_analysis_tool

consultant = Agent(
	name="consultant",
	model=gpt,
	instructions=CONSULTANT_INSTRUCTION,
	tools=[ReasoningTools(), YFinanceTools(), competitor_analysis_tool],
	response_model=ConsultationOutput
)