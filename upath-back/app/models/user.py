import enum
import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class StatusConta(str, enum.Enum):
    ativo = "ativo"
    inativo = "inativo"
    suspenso = "suspenso"


# >>> Essa enum existe só pro restante do código que ainda espera "Role"
class Role(str, enum.Enum):
    student = "student"
    admin = "admin"


class User(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(
        "id_usuario",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    nome: Mapped[str] = mapped_column(String(150), nullable=False)

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        index=True,
    )

    # no banco está como CHAR(64)
    senha_hash: Mapped[str] = mapped_column(String(64), nullable=False)

    data_cadastro: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow,
    )

    status_conta: Mapped[StatusConta] = mapped_column(
        SAEnum(StatusConta),
        default=StatusConta.ativo,
    )

    # ---- Compatibilidade com o código antigo ----

    @property
    def role(self) -> Role:
        # TEMP: enquanto não ligar com a tabela "perfil",
        # todo mundo é tratado como "student"
        return Role.student

    @property
    def is_active(self) -> bool:
        # usa o status_conta do banco pra dizer se está ativo
        return self.status_conta == StatusConta.ativo
