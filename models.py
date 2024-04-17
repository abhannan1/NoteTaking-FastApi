from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone
from sqlalchemy import Text, Integer, UUID

class Base (DeclarativeBase):
    pass

class Note(Base):
    __tablename__ = "notes"

    id : Mapped[str] = mapped_column(UUID, primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    date_created: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))



    def __repr__(self) -> str:
        return f"note tittled: {self.title}, created at {self.date_created}"