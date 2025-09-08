from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.note import Note
from app.schemas.user import UserResponse
from app.ai.answers import get_answer as get_ai_answer
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user

router = APIRouter()


@router.post('/{note_id}/answer', status_code=status.HTTP_200_OK)
async def get_answer(note_id: str, user: UserResponse = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Note).where(Note.id == note_id, Note.author_id == user.id))
        note = result.scalar_one_or_none()
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
            
        answer = get_ai_answer(note.title, note.content)
        
        return {
            "message": "Answer retrieved successfully",
            "data": answer
        }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )