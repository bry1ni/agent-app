import os


def load_prompt(file_path):
	"""
	Load the content of a `.md` file as a string.

	Args:
	    file_path (str): Path to the markdown file.

	Returns:
	    str: Content of the file.
	"""
	if not os.path.exists(file_path):
		raise FileNotFoundError(f"The file {file_path} does not exist.")
	with open(file_path, encoding="utf-8") as file:
		return file.read()