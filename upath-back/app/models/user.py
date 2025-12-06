import enum
import datetime
import uuid

from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, Boolean, DateTime

from app.db.base import Base


class Role(str, enum.Enum):
    student = "student"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    # Agora o id é string (UUID em texto), compatível com MySQL/MariaDB
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    # 'nome' no código, 'full_name' na tabela
    nome: Mapped[str] = mapped_column("full_name", String(120))

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    # 'senha_hash' no código, 'hashed_password' na tabela
    senha_hash: Mapped[str] = mapped_column("hashed_password", String(255))

    # Enum com nome explícito (bom para MySQL)
    role: Mapped[Role] = mapped_column(
        Enum(Role, name="role_enum"),
        default=Role.student,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # 'criado_em' no código, 'created_at' na tabela
    criado_em: Mapped[datetime.datetime] = mapped_column(
        "created_at",
        DateTime(timezone=False),
        default=datetime.datetime.utcnow,
    )
