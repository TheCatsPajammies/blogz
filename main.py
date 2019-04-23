from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:badgerbadger@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'asdf1234lkj987'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    date = db.Column(db.Date())
    body = db.Column(db.String(4000))

    def __init__(self, title, date, body):
        self.title = title
        self.date = date
        self.body = body

@app.route('/')
def index():
    
    blogs = Blog.query.all()

    return render_template('index.html', title="Build a Blog!", blogs=blogs)

@app.route('/new-blog', methods=['POST','GET'])
def new_entry():
    if request.method == 'POST':
        title = request.form['title']
        today = str(date.today())
        body = request.form['body']
        
        blog_entry = Blog(title, today, body)
        db.session.add(blog_entry)
        db.session.commit()
        return redirect('/')

    return render_template('new-blog.html', title="Add a Blog Entry")


if __name__ == "__main__":
    app.run()