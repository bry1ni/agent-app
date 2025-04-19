import requests
from src.tasks import EMAIL_AUTH, PASSWORD_AUTH, API_BASE

def get_token() -> str:
    r = requests.post(f"{API_BASE}/auth/jwt/create/", json={"email": EMAIL_AUTH, "password": PASSWORD_AUTH})
    r.raise_for_status()
    return r.json()["access"]

def auth_hdr(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}