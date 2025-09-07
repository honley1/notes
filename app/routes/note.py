from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.models.note import Note
from app.models.user import User
from app.schemas.note import NoteRequest, NoteResponse
from app.schemas.user import UserResponse

router = APIRouter()

@router.get('/')
async def get_notes(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Note).where(Note.author_id == user.id))
        notes = result.scalars().all()
        return {
            "message": "Notes retrieved successfully",
            "data": [NoteResponse.model_validate(note) for note in notes]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post('/')
async def create_note(note_data: NoteRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        note = Note(
            **note_data.model_dump(),
            author_id=user.id
        )

        db.add(note)
        await db.commit()
        await db.refresh(note)

        new_note = NoteResponse.model_validate(note)
        new_note.author = UserResponse.model_validate(user)

        return {
            "message": "Note created successfully",
            "data": NoteResponse.model_validate(new_note)
        }
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )