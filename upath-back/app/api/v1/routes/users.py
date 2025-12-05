# app/api/v1/routes/users.py
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/home")
async def home(user: User = Depends(get_current_user)):
    cards = [
        {"titulo": "Sisu abre hoje", "descricao": "Confira prazos e notas", "imagem": "https://.../img1.jpg"},
        {"titulo": "Novas bolsas", "descricao": "Veja oportunidades", "imagem": "https://.../img2.jpg"},
    ]
    return {
        "success": True,
        "data": {
            "nome": user.nome,  # se quiser usar o nome real
            "imagem": "https://.../foto.jpg",
            "cards": cards,
        },
    }


@router.get("/profile")
async def profile(user: User = Depends(get_current_user)):
    return {
        "success": True,
        "user": {   # 👈 casa com o que o HomeUser espera: data.user.nome
            "id": str(user.id),
            "nome": user.nome,
            "email": user.email,
            "ultimo_login": "2025-10-27T12:34:56Z",  # placeholder por enquanto
        },
    }


@router.put("/profile")
async def update_profile(body: dict, user: User = Depends(get_current_user)):
    # ainda é mock; quando quiser, pode usar body para atualizar coisas simples
    return {"success": True, "data": {"message": "Perfil atualizado"}}


@router.put("/password")
async def change_password(body: dict, user: User = Depends(get_current_user)):
    return {"success": True, "data": {"message": "Senha alterada"}}


@router.post("/logout")
async def logout(user: User = Depends(get_current_user)):
    # JWT é stateless, então só devolvemos sucesso
    return {"success": True, "data": {"message": "Logout efetuado"}}
