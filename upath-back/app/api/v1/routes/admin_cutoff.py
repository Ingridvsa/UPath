# app/api/v1/routes/admin_cutoff.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator
from app.api.deps import require_admin
from app.models.cutoff import Cutoff
from app.api.deps import db_dep
import re, datetime

router = APIRouter(prefix="/admin", tags=["admin-cutoff"])

class CutoffIn(BaseModel):
    nome_instituicao: str
    nome_curso: str
    estado: str
    modalidade: str
    ano: int
    nova_nota_corte: float
    @field_validator("estado")
    @classmethod
    def sigla(cls, v): 
        if not re.fullmatch(r"[A-Z]{2}", v): raise ValueError("Estado deve ser UF (ex: PE)."); return v
    @field_validator("modalidade")
    @classmethod
    def mod(cls, v): 
        if v not in ("ampla","cota"): raise ValueError("modalidade inválida"); return v
    @field_validator("ano")
    @classmethod
    def ano_ok(cls, v): 
        if v < 2000: raise ValueError("ano inválido"); return v
    @field_validator("nova_nota_corte")
    @classmethod
    def nota_ok(cls, v): 
        if v < 0 or v > 1000: raise ValueError("nota_corte deve estar entre 0 e 1000"); return v

@router.post("/cutoff/update")
async def cutoff_update(body: CutoffIn, admin=Depends(require_admin), db=Depends(db_dep)):
    rec = Cutoff(
        nome_instituicao=body.nome_instituicao,
        nome_curso=body.nome_curso,
        estado=body.estado,
        modalidade=body.modalidade,
        ano=body.ano,
        nota_corte=body.nova_nota_corte,
        atualizado_por="{} (admin)".format(admin["sub"]),
        data_atualizacao=datetime.datetime.utcnow()
    )
    db.add(rec); await db.commit()
    return {"success": True, "data": {"mensagem":"Tudo pronto, agora as simulações passam a usar os novos dados!", "ultima_atualizacao": rec.data_atualizacao.isoformat(), "atualizado_por": rec.atualizado_por}}

@router.get("/cutoff/last-update")
async def cutoff_last(admin=Depends(require_admin), db=Depends(db_dep)):
    # stub: retornar o último (ordem por data desc)
    return {"success": True, "data": {"nome_instituicao":"UFPE","nome_curso":"Direito","ano":2025,"modalidade":"ampla","nota_corte":715.6,"data_atualizacao":"2025-10-29T14:37:22Z","atualizado_por":"Ana Souza"}}
