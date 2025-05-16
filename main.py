from agno.playground import Playground, serve_playground_app

from src.agents.agent import agent

app = Playground(
        agents=[agent],
        teams=[],
    ).get_app()

if __name__ == "__main__":
    serve_playground_app("main:app", reload=True)
    
