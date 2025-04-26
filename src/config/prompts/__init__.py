import os

from .utils import load_prompt

# Define paths to the `.md` files
PROMPTS_DIR = os.path.dirname(__file__)
AGENT_INSTRUCTION_PATH = os.path.join(PROMPTS_DIR, "agent.md")

# Load prompts
AGENT_INSTRUCTION = load_prompt(AGENT_INSTRUCTION_PATH)