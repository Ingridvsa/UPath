# app/api/v1/routes/tests.py
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.services.ia_service import ia_next_question, ia_result
router = APIRouter(prefix="/tests", tags=["tests"])

@router.get("/")
async def list_tests(user=Depends(get_current_user)):
    return {"success": True, "data": [{"id":1,"nome":"Teste IA 8 perguntas"}]}

@router.post("/{id}/start")
async def start_test(id: int, body: dict | None = None, user=Depends(get_current_user)):
    q = await ia_next_question({"start": True})
    return {"success": True, "data": {"test_id": 123, "pergunta": q}}

@router.post("/{test_id}/question-response")
async def answer(test_id: int, body: dict, user=Depends(get_current_user)):
    q = await ia_next_question({"resposta": body.get("resposta")})
    return {"success": True, "data": {"proxima_pergunta": q}}

@router.post("/{test_id}/finish")
async def finish(test_id: int, body: dict | None = None, user=Depends(get_current_user)):
    res = await ia_result({"respostas": body.get("respostas", [])})
    return {"success": True, "data": res}

@router.get("/history")
async def history(user=Depends(get_current_user)):
    return {"success": True, "data": []}

@router.get("/{id}")
async def get_test(id: int, user=Depends(get_current_user)):
    return {"success": True, "data": {"id": id}}
