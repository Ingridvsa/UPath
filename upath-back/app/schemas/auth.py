# app/api/v1/schemas/auth.py
import re
from typing import Optional, Dict, Any, Annotated
from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    StringConstraints,
    Field,
    AliasChoices,
    ConfigDict,
)

NOME_RE = re.compile(r'^[A-Za-zÀ-ÿ\s]+$')
SENHA_RE = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,}$')

SenhaType = Annotated[str, StringConstraints(min_length=8, max_length=72)]


class RegisterIn(BaseModel):
    nome: str
    email: EmailStr
    confirmEmail: EmailStr
    senha: SenhaType
    confirmSenha: str

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v: str) -> str:
        v = v.strip()
        if not NOME_RE.fullmatch(v):
            raise ValueError("Nome inválido.")
        return v

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v: str) -> str:
        if not SENHA_RE.fullmatch(v):
            raise ValueError("Senha fraca.")
        if len(v.encode("utf-8")) > 72:
            raise ValueError("A senha não pode ter mais de 72 caracteres.")
        return v

    @field_validator("confirmEmail")
    @classmethod
    def emails_iguais(cls, v: EmailStr, info):
        if v != info.data.get("email"):
            raise ValueError("Emails não coincidem.")
        return v

    @field_validator("confirmSenha")
    @classmethod
    def senhas_iguais(cls, v: str, info):
        if v != info.data.get("senha"):
            raise ValueError("Senhas não coincidem.")
        return v


class RegisterOut(BaseModel):
    success: bool = True
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class LoginIn(BaseModel):
    email: EmailStr
    senha: str


class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]


class ForgotPasswordIn(BaseModel):
    email: EmailStr


class ForgotPasswordOut(BaseModel):
    success: bool = True
    message: str
    # em DEV vamos devolver o token pra você ver
    reset_token: Optional[str] = None


class ResetPasswordIn(BaseModel):
    token: str
    senha: SenhaType
    confirmSenha: str

    @field_validator("confirmSenha")
    @classmethod
    def senhas_iguais(cls, v: str, info):
      if v != info.data.get("senha"):
          raise ValueError("Senhas não coincidem.")
      return v


class ResetPasswordOut(BaseModel):
    success: bool = True
    message: str