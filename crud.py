from models import Note
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select



# crud.py
from sqlalchemy.future import select  # Import the correct 'select' from 'sqlalchemy.future'

class CRUD:
    async def get_all_notes(self, session: AsyncSession):
        stmt = select(Note).order_by(Note.id)
        result = await session.execute(stmt)
        return result.scalars()

    async def get_by_id(self, session: AsyncSession, note_id: str):
        stmt = select(Note).filter(Note.id == note_id)
        result = await session.execute(stmt)
        return result.scalars().one()

    async def add(self, session: AsyncSession, note: Note):
        session.add(note)
        await session.commit()
        return note

    async def update(self, session: AsyncSession, note_id: str, data):
        statement = select(Note).filter(Note.id == note_id)
        result = await session.execute(statement)
        note = result.scalars().one()
        note.title = data["title"]
        note.content = data["content"]
        await session.commit()
        return note

    async def delete(self, session: AsyncSession, note: Note):
        await session.delete(note)
        await session.commit()
        return {}


# class CRUD:
#     async def get_all_notes(self, async_session: async_sessionmaker[AsyncSession]):
#         """
#         get all note objects in the database
#         """

#         async with async_session() as session:
#             stmt= select(Note).order_by(Note.id)
#             result = await session.execute(stmt)

#         return result.scalars()
    
#     async def add (self, async_session: async_sessionmaker[AsyncSession], note:Note):
#         async with async_session() as session:
#             session.add(note)
#             await session.commit()

#         return note
    
#     async def get_by_id(self, async_session: async_sessionmaker[AsyncSession], note_id:str):
#         async with async_session() as session:
#             stmt = select(Note).filter(Note.id == note_id)
#             result = await session.execute(stmt)

#             return result.scalars().one()

#     async def update(self, async_session: async_sessionmaker[AsyncSession], note_id:str , data):
#         async with async_session() as session:
#             statement = select(Note).filter(Note.id == note_id)

#             result = await session.execute(statement)

#             note = result.scalars().one()

#             note.title = data["title"]
#             note.content = data["content"]

#             await session.commit()

#             return note
        
#     async def delete(self, async_session: async_sessionmaker[AsyncSession], note: Note):
#         """
#         delete note by id
#         """
#         async with async_session() as session:
#             await session.delete(note)
#             await session.commit()

#         return {}