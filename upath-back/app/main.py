# main.py
import sys
import asyncio

# 🔥 Correção necessária para Windows + Psycopg Async funcionar
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# App principal
app = FastAPI(title=settings.PROJECT_NAME)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Subaplicação para /api/v1
api = FastAPI()


def safe_include(module_name):
    """
    Carrega routers existentes e ignora módulos quebrados.
    """
    try:
        module = __import__(f"app.api.v1.routes.{module_name}", fromlist=["router"])
        api.include_router(module.router)
        print(f"[OK] Router carregado: {module_name}")
    except Exception as e:
        print(f"[IGNORADO] {module_name}: {e}")


# ROTAS
rotas = [
    "auth",
    "admin_courses",
    "admin_cutoff",
    "admin_reports",
    "notifications",
    "tests",
    "simulation",
    "users",
    "ia_proxy",
]

for r in rotas:
    safe_include(r)

app.mount(settings.API_V1_PREFIX, api)

# Healthcheck
@app.get("/health")
async def health():
    return {"status": "ok"}
