# app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.core.config import settings
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

bearer = HTTPBearer(auto_error=True)

async def db_dep() -> AsyncSession:
    async for s in get_db():
        yield s

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    try:
        payload = jwt.decode(creds.credentials, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        return payload  # {"sub": email, "role": "..."}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

def require_admin(user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user
