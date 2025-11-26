# app/api/v1/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.auth import (
    RegisterIn,
    RegisterOut,
    LoginIn,
    LoginOut,
)
from app.models.user import User, Role
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


# ---------- REGISTER ---------- #

@router.post("/register", response_model=RegisterOut, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterIn, db: AsyncSession = Depends(get_db)):
    # verifica se já existe usuário com esse e-mail
    exists = await db.execute(
        select(User.id).where(User.email == payload.email.lower())
    )
    if exists.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já cadastrado.",
        )

    user = User(
        nome=payload.nome,
        email=payload.email.lower(),
        senha_hash=hash_password(payload.senha),
        role=Role.student,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {
        "success": True,
        "data": {"nome": user.nome, "email": user.email},
        "error": None,
    }


# ---------- LOGIN ---------- #

@router.post("/login", response_model=LoginOut)
async def login(payload: LoginIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.email == payload.email.lower())
    )
    user: User | None = result.scalar_one_or_none()

    if not user or not verify_password(payload.senha, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo.",
        )

    token = create_access_token(sub=str(user.id), role=user.role.value)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "nome": user.nome,
            "email": user.email,
            "role": user.role.value,
        },
    }
