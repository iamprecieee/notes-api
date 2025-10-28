from models.note import Note
from core.exceptions import ForbiddenError, NotFoundError


class NoteService:
    async def create_note(
        self, title: str, content: str, user_id: str, org_id: str, user_role: str
    ) -> Note:
        if user_role not in ["writer", "admin"]:
            raise ForbiddenError(
                status_code=403, detail="Only writers and admins can create notes"
            )

        note = Note(
            title=title,
            content=content,
            author_id=user_id,
            org_id=org_id,
        )
        await note.insert()
        return note

    async def list_notes(
        self, org_id: str, limit: int = 20, offset: int = 0
    ) -> tuple[list[Note], int]:
        notes = (
            await Note.find(Note.org_id == org_id).skip(offset).limit(limit).to_list()
        )
        total = await Note.find(Note.org_id == org_id).count()
        return notes, total

    async def get_note(self, note_id: str, org_id: str) -> Note:
        note = await Note.get(note_id)
        if not note:
            raise NotFoundError(status_code=404, detail="Note not found")

        if note.org_id != org_id:
            raise NotFoundError(status_code=404, detail="Note not found")

        return note

    async def delete_note(self, note_id: str, org_id: str, user_role: str) -> None:
        if user_role != "admin":
            raise ForbiddenError(status_code=403, detail="Only admins can delete notes")

        note = await Note.get(note_id)
        if not note:
            raise NotFoundError(status_code=404, detail="Note not found")

        if note.org_id != org_id:
            raise NotFoundError(status_code=404, detail="Note not found")

        await note.delete()
