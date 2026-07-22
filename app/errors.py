from flask import render_template
from app import app, database

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errorPages/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    database.session.rollback() # Issue a session rollback to make sure any failed database session do not interfere with any database accessses triggered by the template. This resets the session to a clean state
    return render_template('errorPages/500.html'), 500