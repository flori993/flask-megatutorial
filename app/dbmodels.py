from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import database as db

class User(db.Model):
    __tablename__ = 'user' # example of how to force a name for a table
    uid: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True, unique= True
    )
    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True
    )
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    # storing password hashes for better security

    # Relations
    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author'
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(150))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc)
        # preventing some date-time headache by defaulting to UTC
    )
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(User.uid), index=True
        # Since not all databases automatically create an index for
        # foreign keys, the index=True option is added explicitly, 
        # so that searches based on this column are optimized.
    )

    # Relations
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    