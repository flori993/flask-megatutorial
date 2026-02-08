from flask import render_template
from app import app

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