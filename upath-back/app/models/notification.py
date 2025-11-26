# app/models/notification.py
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, Enum, DateTime, ForeignKey
from app.db.base import Base
import enum, datetime

class NotifTipo(str, enum.Enum):
    prazo="prazo"; status="status"; alerta="alerta"; bolsa="bolsa"; curso="curso"; nota="nota"

class Notification(Base):
    __tablename__="notifications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    titulo: Mapped[str] = mapped_column(String(200))
    tipo: Mapped[NotifTipo] = mapped_column(Enum(NotifTipo))
    lido: Mapped[bool] = mapped_column(Boolean, default=False)
    data_envio: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    descricao_curta: Mapped[str | None] = mapped_column(String(300), nullable=True)

class NotificationSettings(Base):
    __tablename__="notification_settings"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    areas: Mapped[str | None] = mapped_column(String(200))      # csv: saude,tech,humanas
    programas: Mapped[str | None] = mapped_column(String(200))  # csv: sisu,prouni
    ativado: Mapped[bool] = mapped_column(Boolean, default=True)
