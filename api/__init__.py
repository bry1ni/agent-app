from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

APP_TITLE = "DLM"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "DLM works to help your business scale"


app = FastAPI(
	title=APP_TITLE,
	version=APP_VERSION,
	description=APP_DESCRIPTION,
	# docs_url=None,  # disable the doc to call it with a lock behind a simple auth
	# redoc_url=None,
	# openapi_url=None,
)

from api import endpoints

app.include_router(endpoints.router)
app.include_router(endpoints.root_router)

origins = [
    "http://localhost:5173",  # Your frontend origin
    "https://storm-api-b2zj.onrender.com",  # Your API origin
    "*"  # For development, you might want to remove this in production
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])