from fastapi import HTTPException

class ServiceNotSupported(Exception):
	def __init__(self, sevice_name):
		self.message = f"{sevice_name} is not supported."
		super().__init__(self.message)

class ServiceNotSupported(HTTPException):
	def __init__(self, message):
		self.message = message
		super().__init__(status_code=500, detail=self.message)

def exception_handler(exception):
	if isinstance(exception, ServiceNotSupported):
		raise ServiceNotSupported(exception.message)

	else:
		raise HTTPException(status_code=500, detail="Unknown Internal Server Error")