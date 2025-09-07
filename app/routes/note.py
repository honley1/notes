from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.models.note import Note
from app.schemas.note import NoteRequest, NoteResponse
from app.schemas.user import UserResponse

router = APIRouter()

@router.get('/')
async def get_notes(user: UserResponse = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Note).options(joinedload(Note.author)).where(Note.author_id == user.id))
        notes = result.scalars().all()
        return {
            "message": "Notes retrieved successfully",
            "data": [NoteResponse.model_validate(note) for note in notes]
        }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post('/')
async def create_note(note_data: NoteRequest, user: UserResponse = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        note = Note(
            **note_data.model_dump(),
            author_id=user.id
        )

        db.add(note)
        await db.commit()
        await db.refresh(note)

        result = await db.execute(select(Note).options(joinedload(Note.author)).where(Note.id == note.id))
        new_note = result.scalar_one()

        return {
            "message": "Note created successfully",
            "data": NoteResponse.model_validate(new_note)
        }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get('/{note_id}')
async def get_note(note_id: str, user: UserResponse = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Note)
            .options(joinedload(Note.author))
            .where(Note.id == note_id, Note.author_id == user.id))
        note = result.scalar_one_or_none()
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )

        return {
            "message": "Note retrieved successfully",
            "data": NoteResponse.model_validate(note)
        }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put('/{note_id}', status_code=status.HTTP_200_OK)
async def update_note(note_id: str, note_data: NoteRequest, user: UserResponse = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Note).where(Note.id == note_id, Note.author_id == user.id))
        note = result.scalar_one_or_none()
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )

        if note_data.title:
            note.title = note_data.title
        if note_data.content:
            note.content = note_data.content

        await db.commit()
        await db.refresh(note)

        result = await db.execute(
            select(Note)
            .options(joinedload(Note.author))
            .where(Note.id == note_id)
        )
        updated_note = result.scalar_one()

        return {
            "message": "Note updated successfully",
            "data": NoteResponse.model_validate(updated_note)
        }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete('/{note_id}', status_code=status.HTTP_200_OK)
async def delete_note(note_id: str, user: UserResponse = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Note).where(Note.id == note_id, Note.author_id == user.id))
        note = result.scalar_one_or_none()
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )

        await db.delete(note)
        await db.commit()

        result = await db.execute(
            select(Note)
            .options(joinedload(Note.author))
            .where(Note.id == note_id))
        deleted_note = result.scalar_one()

        return {
            "message": "Note deleted successfully",
            "data": NoteResponse.model_validate(deleted_note)
        }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )