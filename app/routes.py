from turtle import title
from wtforms import form
from flask import render_template, flash, redirect, url_for, request
from app import app
from app import database as db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.dbmodels import User
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
import sqlalchemy as sa
from datetime import datetime, timezone

@app.route("/")
@app.route("/index")
@login_required # Some stuff may be protected with this argument from anonymous users!
def index():
    posts = [
        {
            'author': {'username': 'Miguel'},
            'body': 'Beauriful day in Montreal!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Shrek movie was so cool!'
        },
        {
            'author' : {'username': 'Megan'},
            'body': 'Coding is not for the weak 🥀'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=["GET", "POST"]) # "methods" argument in the route decorator, this tells Flask that this view function accepts GET and POST requests, overriding the default, which is to accept only GET requests
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            # Checks if there's any next page OR an absolute URL to be rejected
            # (for a better security against malicious site in "next" argument)
            next_page = url_for('index')
        return redirect(next_page) # Redirect only to the relative URL

    return render_template('login.html', title = "Sign in", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you\'re now a registered user!')
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>') # <username> is a dynamic component for the URL
@login_required # make this function accessible only to users logged in, so no-one else with the link could access profile
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
        # Interesting fact, the reason why there's no db.session.add() before 
        # commit() is because when current_user is referenced, Flask-Login 
        # will invoke the user loader callback function, which will run a 
        # database query that will put the target user in the database session.
        # The user may be added again in this function, but it's not necessary 
        # because it's already there

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    _form = EditProfileForm(current_user.username)
    if _form.validate_on_submit():
        current_user.username = _form.username.data
        current_user.about_me = _form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        _form.username.data = current_user.username
        _form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit profile', form=_form)