from model.configuration import Configuration

import json
import logging
from fastapi import APIRouter, Request, Response ,status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/healthcheck")
async def healthcheck():
    return "OK"

config = Configuration.get_config()

# line
@router.post("/line", status_code=status.HTTP_200_OK)
async def line_webhook(request: Request, response: Response):
    request_body = json.loads(await request.body())

    return JSONResponse(content={"code": 200, "message": "ok"}, status_code=status.HTTP_200_OK)
    
@router.post("/rocket", status_code=status.HTTP_200_OK)
async def rocket_webhook(request: Request, response: Response):
    request_body = json.loads(await request.body())
    print(request_body)
    return JSONResponse(content={"code": 200, "message": "ok"}, status_code=status.HTTP_200_OK)
    