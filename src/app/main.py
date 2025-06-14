import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.app.domain.auth import router as auth_router
from src.app.config.config import settings

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "resource" / "static"

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=auth_router, prefix=settings.API_V1_STR)

@app.get("/")
async def health_check():
    return JSONResponse({"status": "ok"})


# test
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
