# app/models/course.py
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Enum
from app.db.base import Base
import enum

class TipoInst(str, enum.Enum):
    publica="publica"; privada="privada"

class Course(Base):
    __tablename__="courses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(200), index=True)
    area: Mapped[str] = mapped_column(String(100))
    instituicao: Mapped[str] = mapped_column(String(200))
    estado: Mapped[str] = mapped_column(String(2))
    duracao_anos: Mapped[int] = mapped_column(Integer)
    valor: Mapped[float] = mapped_column(Float, default=0.0)
    tipo_instituicao: Mapped[TipoInst] = mapped_column(Enum(TipoInst), default=TipoInst.publica)

class Scholarship(Base):
    __tablename__="scholarships"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(Integer)
    programa: Mapped[str] = mapped_column(String(50))  # PROUNI...
    percentual_desconto: Mapped[int] = mapped_column(Integer)    # 50 | 100
