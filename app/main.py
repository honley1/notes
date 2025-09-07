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

app.include_router(api)
