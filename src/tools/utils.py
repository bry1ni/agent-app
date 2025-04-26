import json
from typing import Any


def format_tool_output(tool_message: Any) -> str:
	"""
	Formats the tool message into a JSON string ensuring it's always a valid str.

	Args:
	    tool_message (Any): The tool message to be converted (typically a dict).

	Returns:
	    str: JSON formatted string representation of the tool message.
	"""
	return json.dumps(tool_message, ensure_ascii=False)
