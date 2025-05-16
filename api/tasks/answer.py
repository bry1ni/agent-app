from src.agents.utils import extract_response_from_agent
from src.agents.agent import agent
from src.models.pydantic_models import Answer

def answer(request: str) -> Answer:
    
    try:
        response = agent.run(
            request
        )
        result = extract_response_from_agent(response, "agent")
        return Answer(**result)
            
    except Exception as e:
        return str(e)