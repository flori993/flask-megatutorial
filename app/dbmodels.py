from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import database as db
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

class User(UserMixin, db.Model):
    __tablename__ = 'user' # Example of how to force a name for a table
    uid: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True, unique= True
    )
    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True
    )
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256)) # Storing password hashes for better security
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )


    # Relations
    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author'
    )

    # Funtions
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_id(self):
        # Because I (Mykyta) made custom name for user id (uid) instead of just
        # calling it "id", I need to override the default implementation for the 
        # method "get_id" that Flask-Login expects user objects to have from mixins.py
        return str(self.uid)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
    # id passed by Flask-Login in function argument is a string, so databases 
    # that use numeric ID need need conversions from str to int.

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(150))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc) # preventing some date-time headache by defaulting to UTC
        
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
    