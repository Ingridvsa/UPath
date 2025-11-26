# app/api/v1/routes/admin_auth.py
from fastapi import APIRouter, Depends
from app.core.security import hash_password, create_access_token, verify_password
from app.api.deps import db_dep
import secrets, datetime
from app.models.user import User, Role
from app.models.user import Admin2FASession
from sqlalchemy import select

router = APIRouter(prefix="/admin", tags=["admin-auth"])

@router.post("/login")
async def admin_login(body: dict, db=Depends(db_dep)):
    email = (body.get("email") or "").lower()
    senha = body.get("senha") or ""
    row = await db.execute(select(User).where(User.email==email, User.role==Role.admin))
    adm = row.scalar_one_or_none()
    if not adm or not verify_password(senha, adm.senha_hash):
        return {"success": False, "error": "Credenciais incorretas."}
    session_id = secrets.token_hex(16)
    pin_plain = "1234"  # no MVP, fixo; em prod: gerar e enviar por email
    sess = Admin2FASession(session_id=session_id, email=email, pin_hash=hash_password(pin_plain), expires_at=datetime.datetime.utcnow()+datetime.timedelta(minutes=10))
    db.add(sess); await db.commit()
    return {"success": True, "data": {"session_id": session_id}}

@router.post("/2fa")
async def admin_2fa(body: dict, db=Depends(db_dep)):
    session_id = body.get("session_id")
    token_4d = body.get("token_4d")
    row = await db.execute(select(Admin2FASession).where(Admin2FASession.session_id==session_id))
    sess = row.scalar_one_or_none()
    if not sess or sess.expires_at < datetime.datetime.utcnow():
        return {"success": False, "error": "Sessão inválida ou expirada."}
    if not verify_password(token_4d, sess.pin_hash):
        return {"success": False, "error": "PIN incorreto."}
    jwt_admin = create_access_token(sub=sess.email, role="admin")
    return {"success": True, "data": {"token": jwt_admin}}
