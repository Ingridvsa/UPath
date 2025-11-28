
import sys
import asyncio
import uvicorn

if sys.platform.startswith("win"):
    # necessário para o psycopg async funcionar no Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,  # opcional: hot reload
    )
