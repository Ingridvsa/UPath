# app/api/v1/routes/ia_proxy.py
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.services.ia_service import ia_result
router = APIRouter(prefix="/ia", tags=["ia"])

@router.post("/predict")
async def predict(body: dict, user=Depends(get_current_user)):
    return {"success": True, "data": await ia_result(body)}

@router.post("/chat")
async def chat(body: dict, user=Depends(get_current_user)):
    return {"success": True, "data": {"resposta":"Entendido! Vamos começar seu teste vocacional.","contexto":"sessao_123"}}
