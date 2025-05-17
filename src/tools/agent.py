from agno.tools import tool


@tool
def this_is_a_tool(tool_input: str) -> str:
    """
    Tool description
    """
    return "Tool response"

def this_is_not_a_tool(tool_input: str) -> str:
    """
    This is not a tool
    """
    return "This is not a tool"