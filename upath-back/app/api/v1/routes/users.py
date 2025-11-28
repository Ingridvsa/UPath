# app/api/v1/routes/users.py
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
router = APIRouter(prefix="/user", tags=["user"])

@router.get("/home")
async def home(user=Depends(get_current_user)):
    cards = [
      {"titulo":"Sisu abre hoje", "descricao":"Confira prazos e notas", "imagem":"https://.../img1.jpg"},
      {"titulo":"Novas bolsas", "descricao":"Veja oportunidades", "imagem":"https://.../img2.jpg"}
    ]
    return {"success": True, "data": {"nome": "Exemplo", "imagem": "https://.../foto.jpg", "cards": cards}}

@router.get("/profile")
async def profile(user=Depends(get_current_user)):
    return {"success": True, "data": {"id_usuario": 1, "nome":"Fulano", "email":"fulano@example.com","foto_url":"https://...","ultimo_login":"2025-10-27T12:34:56Z"}}

@router.put("/profile")
async def update_profile(body: dict, user=Depends(get_current_user)):
    return {"success": True, "data": {"message": "Perfil atualizado"}}

@router.put("/password")
async def change_password(body: dict, user=Depends(get_current_user)):
    return {"success": True, "data": {"message": "Senha alterada"}}

@router.post("/logout")
async def logout(user=Depends(get_current_user)):
    return {"success": True, "data": {"message": "Logout efetuado"}}
