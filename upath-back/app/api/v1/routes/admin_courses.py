# app/api/v1/routes/admin_courses.py
from fastapi import APIRouter, Depends, Query
from app.api.deps import require_admin
router = APIRouter(prefix="/admin", tags=["admin-courses"])

@router.get("/courses")
async def list_courses(q: str | None = None, estado: str | None = None, area: str | None = None, page: int = 1, admin=Depends(require_admin)):
    return {"success": True, "data": [{"id_curso":101,"nome":"Enfermagem","area":"Saúde","instituicao":"UPE","estado":"PE","duracao_anos":5,"valor":0.0,"tipo_instituicao":"publica"}]}

@router.get("/courses/{cid}")
async def get_course(cid: int, admin=Depends(require_admin)):
    return {"success": True, "data": {"id_curso": cid}}

@router.post("/courses")
async def upsert_course(body: dict, admin=Depends(require_admin)):
    return {"success": True, "data": {"id_curso": 123, "mensagem":"Curso salvo com sucesso."}}

@router.delete("/courses/{cid}")
async def delete_course(cid: int, admin=Depends(require_admin)):
    return {"success": True, "data": {"mensagem":"Curso excluído"}}

@router.post("/courses/{cid}/scholarship")
async def link_scholarship(cid: int, body: dict, admin=Depends(require_admin)):
    return {"success": True, "data": {"mensagem": f"Bolsa {body.get('programa')} ({body.get('percentual_desconto')}%) vinculada ao curso."}}

@router.delete("/courses/{cid}/scholarship")
async def unlink_scholarship(cid: int, admin=Depends(require_admin)):
    return {"success": True, "data": {"mensagem":"Bolsa desvinculada"}}
