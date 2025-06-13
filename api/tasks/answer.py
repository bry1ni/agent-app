from src.agents.utils import extract_response_from_agent, getAgentAnswer, create_agent
from src.agents.agent import agent
from src.models.pydantic_models import Answer

def answer(request: str) -> Answer:
    """
    Answer a question using the agent.
    """
    query = request.query
    
    try:
        agent_ = create_agent(**vars(agent))
        response = getAgentAnswer(agent_, query)
        result = extract_response_from_agent(response, "agent")
        return Answer(**result)
            
    except Exception as e:
        return str(e)