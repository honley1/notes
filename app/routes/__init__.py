from fastapi import APIRouter
from .auth import router as auth_router
from .note import router as note_router
from .ai import router as ai_router

api = APIRouter(prefix="/api")
api.include_router(auth_router, prefix="/auth", tags=["auth"])
api.include_router(note_router, prefix="/notes", tags=["notes"])
api.include_router(ai_router, prefix="/ai", tags=["ai"])