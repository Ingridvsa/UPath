# app/services/ia_service.py
import httpx
from app.core.config import settings

async def ia_next_question(payload: dict):
    async with httpx.AsyncClient(timeout=20) as c:
        # endpoint do teu microserviço: /ia/teste
        r = await c.post(f"{settings.IA_BASE_URL}/ia/teste", json=payload)
        return r.json()

async def ia_result(payload: dict):
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post(f"{settings.IA_BASE_URL}/ia/result", json=payload)
        return r.json()
