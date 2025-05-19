def test_agent_is_running():
    """Test that the agent is running."""
    from src.agents.agent import agent
    assert agent.run("Hello, world!")   