from agno.models.openai import OpenAIChat

gpt = OpenAIChat(
	id="gpt-4o",
	temperature=0.4,
)

AGENT_RESPONSE_KEYS = {
    "consultant": ["summary_report", "recommendations"],
    "executor": ["sql", "action", "action_type", "target", "preview"],
}
