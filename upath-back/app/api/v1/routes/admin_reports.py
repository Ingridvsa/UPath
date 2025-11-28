# app/api/v1/routes/admin_reports.py
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.user import User

router = APIRouter(
    prefix="/admin/reports",
    tags=["admin-reports"],
)


def _periodo_para_dias(periodo: str) -> int:
    """
    Converte '7d', '30d', '90d' para número de dias.
    """
    mapping = {
        "7d": 7,
        "30d": 30,
        "90d": 90,
    }
    if periodo not in mapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Período inválido. Use: 7d, 30d ou 90d.",
        )
    return mapping[periodo]


@router.get("/preview")
async def preview(
    tipo: str,
    periodo: str,
    admin=Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Retorna dados reais para o gráfico e total de usuários.
    Por enquanto implementamos apenas tipo='usuarios'.
    """
    if tipo != "usuarios":
        # se quiser, pode implementar outros tipos depois
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de relatório inválido. Use: 'usuarios' por enquanto.",
        )

    dias = _periodo_para_dias(periodo)
    agora = datetime.utcnow()
    data_inicial = agora - timedelta(days=dias)

    # 1) Total de usuários no sistema
    result_total = await db.execute(
        select(func.count(User.id))
    )
    total_usuarios: int = result_total.scalar_one()

    # 2) Novos usuários por dia no período
    # date_trunc('day', created_at) para agrupar por dia
    result_grafico = await db.execute(
        select(
            func.date_trunc("day", User.criado_em).label("dia"),
            func.count(User.id).label("qtd"),
        )
        .where(User.criado_em >= data_inicial)
        .group_by(func.date_trunc("day", User.criado_em))
        .order_by(func.date_trunc("day", User.criado_em))
    )

    rows = result_grafico.all()

    # Monta labels e valores
    labels = []
    valores = []
    for dia, qtd in rows:
        # dia é datetime, formata para exibição
        labels.append(dia.strftime("%d/%m"))
        valores.append(int(qtd))

    return {
        "success": True,
        "data": {
            "grafico": {
                "labels": labels,
                "valores": valores,
            },
            "total_usuarios": total_usuarios,
            "periodo": periodo,
            "tipo": tipo,
        },
    }


@router.get("/metadata")
async def metadata(admin=Depends(require_admin)):
    """
    Se quiser manter alguma info estática ou complementar.
    Pode depois buscar do banco/logs reais.
    """
    return {
        "success": True,
        "data": {
            "tipo": "usuarios_ativos",
            "gerado_em": datetime.utcnow().isoformat() + "Z",
            "gerado_por": "Painel Admin UPath",
        },
    }
