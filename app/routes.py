from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route("/")
@app.route("/index")
def index():
    user = {'username': 'Mykyta'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=["GET", "POST"]) # "methods" argument in the route decorator, this tells Flask that this view function accepts GET and POST requests, overriding the default, which is to accept only GET requests
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))

    return render_template('login.html', title = "Sign in", form=form)
