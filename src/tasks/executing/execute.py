from fastapi import HTTPException
import requests
from src.tasks.utils import get_token, auth_hdr
from src.tasks import API_BASE, SHOP_ID, PRODUCT_ID

def update_product(payload: dict, id_: str = PRODUCT_ID, shop_id: str = SHOP_ID):
    token = get_token()
    endpoint = f"{API_BASE}/api/shops/{shop_id}/products/{id_}/"

    try:
        response = requests.put(endpoint, json=payload, headers=auth_hdr(token))
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))