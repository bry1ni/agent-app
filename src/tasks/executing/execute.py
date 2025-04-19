from fastapi import HTTPException
import requests
from src.tasks.utils import get_token, auth_hdr
from src.tasks import API_BASE, SHOP_ID

def update_product(payload: dict, id: str, shop_id: str = SHOP_ID):
    token = get_token()
    endpoint = f"{API_BASE}/api/shops/{shop_id}/products/{id}/"

    try:
        response = requests.post(endpoint, json=payload, headers=auth_hdr(token))
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))