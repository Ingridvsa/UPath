from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.user import User, Role
from app.core.security import hash_password, verify_password, create_access_token

async def register_user(payload, db: AsyncSession):
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

    return user


async def login_user(payload, db: AsyncSession):
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

    return token, user
