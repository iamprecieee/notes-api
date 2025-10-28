from typing import Annotated

from fastapi import APIRouter, Depends, Query

from core.dependencies import (
    get_current_user,
    get_note_service,
    CurrentUser,
    NoteService,
)
from schemas.requests import CreateNoteRequest
from schemas.responses import SuccessResponse, NoteResponse, NoteListResponse

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=SuccessResponse)
async def create_note(
    request: CreateNoteRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    service: Annotated[NoteService, Depends(get_note_service)],
):
    note = await service.create_note(
        title=request.title,
        content=request.content,
        user_id=current_user.id,
        org_id=current_user.org_id,
        user_role=current_user.role,
    )

    return SuccessResponse(
        data=NoteResponse(
            id=str(note.id),
            title=note.title,
            content=note.content,
            author_id=note.author_id,
            org_id=note.org_id,
            created_at=note.created_at,
            updated_at=note.updated_at,
        ),
        message="Note created successfully",
    )


@router.get("/", response_model=SuccessResponse)
async def list_notes(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    service: Annotated[NoteService, Depends(get_note_service)],
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    notes, total = await service.list_notes(
        org_id=current_user.org_id,
        limit=limit,
        offset=offset,
    )

    return SuccessResponse(
        data=NoteListResponse(
            notes=[
                NoteResponse(
                    id=str(note.id),
                    title=note.title,
                    content=note.content,
                    author_id=note.author_id,
                    org_id=note.org_id,
                    created_at=note.created_at,
                    updated_at=note.updated_at,
                )
                for note in notes
            ],
            total=total,
        )
    )


@router.get("/{id}", response_model=SuccessResponse)
async def get_note(
    id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    service: Annotated[NoteService, Depends(get_note_service)],
):
    note = await service.get_note(
        note_id=id,
        org_id=current_user.org_id,
    )

    return SuccessResponse(
        data=NoteResponse(
            id=str(note.id),
            title=note.title,
            content=note.content,
            author_id=note.author_id,
            org_id=note.org_id,
            created_at=note.created_at,
            updated_at=note.updated_at,
        )
    )


@router.delete("/{id}", status_code=204)
async def delete_note(
    id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    service: Annotated[NoteService, Depends(get_note_service)],
):
    await service.delete_note(
        note_id=id,
        org_id=current_user.org_id,
        user_role=current_user.role,
    )
