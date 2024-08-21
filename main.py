from fastapi import FastAPI
from api.api import api_router
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GestorLab - Api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://gestorlab.netlify.app","http://127.0.0.1:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)
