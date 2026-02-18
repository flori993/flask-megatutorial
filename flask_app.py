from app import app, database
from app.dbmodels import User, Post
import sqlalchemy as sa
import sqlalchemy.orm as so

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': database, 'User': User, 'Post': Post}

