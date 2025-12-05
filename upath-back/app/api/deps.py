# app/api/deps.py
from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.v1.routes.auth import get_current_user
from app.models.user import User, Role


async def db_dep() -> AsyncGenerator[AsyncSession, None]:
    async for s in get_db():
        yield s


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Garante que o usuário autenticado é admin.
    """
    if current_user.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado",
        )
    return current_user
