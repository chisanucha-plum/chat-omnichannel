from fastapi import APIRouter, FastAPI
import uvicorn
from router import webhook

def get_router() -> APIRouter:
    
    router = APIRouter()
    router.include_router(webhook.router, prefix="/webhook")
    
    return router

def get_app() -> FastAPI:
    
    app = FastAPI()
    app.include_router(get_router())

    return app

app = get_app()

if __name__ == "__main__":
    uvicorn.run(app, port=8001)
