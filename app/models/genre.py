from ..db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy import ForeignKey

class Genre(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    books: Mapped[list["Book"]] = relationship(secondary="book_genre", back_populates="genres")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
    @classmethod
    def from_dict(cls, genre_data):
        new_genre = cls(name=genre_data["name"])
        return new_genre
        
