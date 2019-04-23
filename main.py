from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:badgerbadger@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'asdf1234lkj987'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(4000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('index.html', title="Build a Blog!", blogs=blogs)

@app.route('/new-blog')
def new_entry():
    return render_template('new-blog.html', title="Add a Blog Entry")

if __name__ == "__main__":
    app.run()