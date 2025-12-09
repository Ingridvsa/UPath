import sys
import asyncio
import uvicorn
import os

if sys.platform.startswith("win"):
    # necessário para o psycopg async funcionar no Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8001)),
    )
