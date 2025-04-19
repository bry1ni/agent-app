import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

API_BASE = os.getenv("API_BASE")
EMAIL_AUTH = os.getenv("EMAIL_AUTH")
PASSWORD_AUTH = os.getenv("PASSWORD_AUTH")
SHOP_ID="1b06a2d6-9e4f-4afd-9aa6-aed77b67119e"
PRODUCT_ID="f83b21c1-630d-4d03-8141-7282b911b27b"
