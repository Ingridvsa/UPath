# app/api/v1/routes/simulations.py
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
router = APIRouter(prefix="/simulations", tags=["simulations"])

@router.post("/")
async def create_simulation(body: dict, user=Depends(get_current_user)):
    # calcular notaUsuario (média ponderada) e comparar com notaCorte (mock)
    retorno = {"curso":"Medicina - UFPE","notaUsuario":726.4,"notaCorte":730.0,"chanceIngresso":89.5,"resultado":"Abaixo da nota de corte"}
    return {"success": True, "data": retorno}

@router.get("/{id}")
async def get_simulation(id: int, user=Depends(get_current_user)):
    return {"success": True, "data": {"id_simulacao": id}}

@router.get("/history")
async def history(user=Depends(get_current_user)):
    return {"success": True, "data": []}
