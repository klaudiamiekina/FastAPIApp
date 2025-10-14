from fastapi import APIRouter

from app.api.descriptions import HEALTH_DESCRIPTION
from app.models.schemas import HealthResponse

import requests


router = APIRouter(prefix="/health", tags=["Health"])


@router.get("",
            response_model=HealthResponse,
            summary="Check application and external API status.",
            description=HEALTH_DESCRIPTION)
async def health():
    statuses_dict = {"app_status": "ok", "external_api_status": "ok"}
    try:
        response = requests.get("http://openlibrary.org/books/OL1M.json?m=history", timeout=3)
        if response.status_code != 200:
            statuses_dict["external_api_status"] = "failed"
    except requests.exceptions.RequestException:
        statuses_dict["external_api_status"] = "failed"
    return statuses_dict
