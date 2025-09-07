import time
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.dependencies.database import engine

from app.routes import api

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan, title="Notes API", docs_url="/api/docs")

@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = time.time()
    print("start time:", datetime.fromtimestamp(start_time).isoformat())

    response = await call_next(request)
    
    end_time = time.time()
    print("end time:", datetime.fromtimestamp(end_time).isoformat())
    
    print("response time: ", end_time - start_time)

    return response

app.include_router(api)
