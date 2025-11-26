# app/models/cutoff.py
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float, String, DateTime
from app.db.base import Base
import datetime

class Cutoff(Base):
    __tablename__="cutoffs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome_instituicao: Mapped[str] = mapped_column(String(200))
    nome_curso: Mapped[str] = mapped_column(String(200))
    estado: Mapped[str] = mapped_column(String(2))
    modalidade: Mapped[str] = mapped_column(String(10))  # ampla|cota
    ano: Mapped[int] = mapped_column(Integer)
    nota_corte: Mapped[float] = mapped_column(Float)
    atualizado_por: Mapped[str] = mapped_column(String(120))
    data_atualizacao: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
