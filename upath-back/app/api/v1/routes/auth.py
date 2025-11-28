# app/api/v1/routes/auth.py
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

from app.db.session import get_db
from app.core.config import settings
from app.schemas.auth import (
    RegisterIn,
    RegisterOut,
    LoginIn,
    LoginOut,
    ForgotPasswordIn,
    ForgotPasswordOut,
    ResetPasswordIn,
    ResetPasswordOut,
    UpdateProfileIn,
    UpdateProfileOut,
    AdminPinIn,
    AdminPinOut,
)
from app.models.user import User, Role
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"  # caminho completo do login
)

RESET_TOKEN_EXPIRE_MINUTES = 30


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


@router.post("/forgot-password", response_model=ForgotPasswordOut)
async def forgot_password(payload: ForgotPasswordIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.email == payload.email.lower())
    )
    user: User | None = result.scalar_one_or_none()

    if not user:
        return ForgotPasswordOut(
            success=True,
            message="Se o e-mail estiver cadastrado, você receberá instruções para redefinir a senha.",
            reset_token=None,
        )

    now = datetime.utcnow()
    exp = now + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)

    reset_token = jwt.encode(
        {
            "sub": str(user.id),
            "scope": "password_reset",
            "exp": exp,
            "iat": now,
        },
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALG,
    )

    return ForgotPasswordOut(
        success=True,
        message="Se o e-mail estiver cadastrado, você receberá instruções para redefinir a senha.",
        reset_token=reset_token,  # DEV: devolvendo pra você testar
    )

@router.post("/reset-password", response_model=ResetPasswordOut)
async def reset_password(payload: ResetPasswordIn, db: AsyncSession = Depends(get_db)):
    # valida token
    try:
        token_data = jwt.decode(
            payload.token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALG],
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expirado. Solicite uma nova redefinição de senha.",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido.",
        )

    if token_data.get("scope") != "password_reset":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido para redefinição de senha.",
        )

    user_id = token_data.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido.",
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user: User | None = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )

    user.senha_hash = hash_password(payload.senha)
    await db.commit()

    return ResetPasswordOut(
        success=True,
        message="Senha redefinida com sucesso. Já pode fazer login com a nova senha.",
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autenticado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALG],
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == user_id))
    user: User | None = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise credentials_exception

    return user


@router.put("/me", response_model=UpdateProfileOut)
async def update_me(
    payload: UpdateProfileIn,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    algo_para_atualizar = False

    # Atualiza nome se veio
    if payload.nome is not None and payload.nome.strip():
      current_user.nome = payload.nome.strip()
      algo_para_atualizar = True

    # Atualiza senha se veio
    if payload.senha is not None and payload.senha.strip():
      current_user.senha_hash = hash_password(payload.senha)
      algo_para_atualizar = True

    if not algo_para_atualizar:
        return UpdateProfileOut(
            success=True,
            message="Nenhuma alteração enviada.",
            data={"nome": current_user.nome, "email": current_user.email},
        )

    await db.commit()
    await db.refresh(current_user)

    return UpdateProfileOut(
        success=True,
        message="Perfil atualizado com sucesso.",
        data={
            "nome": current_user.nome,
            "email": current_user.email,
        },
    )


@router.post("/admin-pin", response_model=AdminPinOut)
async def validate_admin_pin(
    payload: AdminPinIn,
    db: AsyncSession = Depends(get_db),
):
    """
    Valida o PIN de administrador e garante que o usuário do e-mail é admin.
    Endpoint final: POST /api/v1/auth/admin-pin
    """

    # 1) Busca usuário pelo e-mail
    result = await db.execute(
        select(User).where(User.email == payload.email.lower())
    )
    user: User | None = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )

    if user.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não é administrador.",
        )

    # 2) Confere o PIN (configurado em settings.ADMIN_PIN / .env)
    if payload.pin != settings.ADMIN_PIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PIN inválido.",
        )

    return AdminPinOut(
        success=True,
        message="PIN validado com sucesso.",
    )