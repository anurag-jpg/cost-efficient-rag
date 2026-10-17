from fastapi import FastAPI

from app.config import settings

app=FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

@app.get("/health")
def health_check():
    return{
        "status":"ok",
        "environment":settings.app_env,
    }