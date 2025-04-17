from agents.executor import executor
from agents.consultant import consultant
from agno.models.openai import OpenAIChat

gpt = OpenAIChat(
	id="gpt-4o",
	temperature=0.4,
)