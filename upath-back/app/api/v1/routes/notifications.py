# app/api/v1/routes/notifications.py
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("/")
async def list_notifications(filter: str | None = None, user=Depends(get_current_user)):
    # filtro: bolsa|curso|nota...
    items = [
      {"id":12,"titulo":"Nova bolsa X","tipo":"bolsa","lido":False,"data_envio":"2025-10-27T18:00:00Z"}
    ]
    return {"success": True, "data": items}

@router.patch("/{nid}/read")
async def mark_read(nid: int, user=Depends(get_current_user)):
    return {"success": True, "data": {"id": nid, "lido": True}}

@router.get("/settings")
async def get_settings(user=Depends(get_current_user)):
    return {"success": True, "data": {"ativado": True, "areas":"saude,tech", "programas":"sisu,prouni"}}

@router.put("/settings")
async def put_settings(body: dict, user=Depends(get_current_user)):
    return {"success": True, "data": {"message": "Configurações salvas"}}
