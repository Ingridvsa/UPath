# app/api/v1/routes/admin_reports.py
from fastapi import APIRouter, Depends
from app.api.deps import require_admin
router = APIRouter(prefix="/admin/reports", tags=["admin-reports"])

@router.get("/preview")
async def preview(tipo: str, periodo: str, admin=Depends(require_admin)):
    return {"success": True, "data": {"grafico":{"labels":["Seg","Ter","Qua","Qui","Sex"],"valores":[10,25,22,30,28]},"total_usuarios":115}}

@router.get("/export")
async def export(tipo: str, periodo: str, formato: str = "pdf", anonimizar: bool = True, admin=Depends(require_admin)):
    # retornar arquivo seria via StreamingResponse; aqui stub JSON
    return {"success": True, "data": {"mensagem": f"Relatório {tipo}/{periodo} exportado como {formato} (anonimizar={anonimizar})."}}

@router.get("/metadata")
async def metadata(admin=Depends(require_admin)):
    return {"success": True, "data": {"tipo":"usuarios_ativos","gerado_em":"2025-10-29T14:45:10Z","gerado_por":"Carlos Mendes"}}
