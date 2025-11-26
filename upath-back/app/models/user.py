import enum
import datetime
import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class Role(str, enum.Enum):
    student = "student"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    # id é UUID na tabela
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,        # gera uuid no app, caso o banco não tenha default
    )

    # 'nome' no código, 'full_name' na tabela
    nome: Mapped[str] = mapped_column("full_name", String(120))

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    # 'senha_hash' no código, 'hashed_password' na tabela
    senha_hash: Mapped[str] = mapped_column("hashed_password", String(255))

    # essa coluna ainda NÃO existe na tabela, vamos criar já já
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.student)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # 'criado_em' no código, 'created_at' na tabela
    criado_em: Mapped[datetime.datetime] = mapped_column(
        "created_at",
        DateTime(timezone=True),
        default=datetime.datetime.utcnow,
    )
