from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from hashybois import make_pw_hash, check_pw_hash
from validate_email import is_email_valid
from datetime import date

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:itmanyblogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'asdf1234lkj987'

def is_session():
    if 'email' in session:
        return True
    return False

class Blog(db.Model):
    ##TODO: owner_id to create relationship to User
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(120))
    date = db.Column(db.Date())
    body = db.Column(db.String(4000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, author, date, body, owner_id):
        self.title = title
        self.author = author
        self.date = date
        self.body = body
        self.owner_id = owner_id

class User(db.Model):
    ##TODO: includes id, username, password, and (blogs) a relationship with Blog
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    pw_hash = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref="user")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.pw_hash = make_pw_hash(password)
    
@app.before_request
def require_login():

    if 'email' in session:
        excepted_routes = ['blog', 'logout']
        if request.endpoint not in excepted_routes:
            email = session['email']
            flash('You are logged in as: ' + email, 'success')
    special_routes = ['newpost']
    if request.endpoint in special_routes and not is_session():
        flash('User must be logged in to write a new entry', 'error')
        return render_template('login.html')

@app.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.order_by(Blog.id.desc()).paginate(page=page, per_page=5)
    users = User.query.all()
    return render_template('index.html', title="Blogz!", blogs=blogs, users=users, is_session=is_session())

@app.route('/blog', methods=['GET'])
def blog():
    id = request.args.get('blog-id')
    author = request.args.get('author')
    if id:
        blog = Blog.query.filter_by(id = id).first()
        return render_template("blog.html", blog=blog, is_session=is_session())
    if author:
        blogs = Blog.query.filter_by(author =author).all()
        return render_template("singleUser.html", blogs=blogs, is_session=is_session())

@app.route('/newpost', methods=['POST','GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        today = str(date.today())
        body = request.form['body']
        if title=="":
            flash("Please give your blog a title", "error")
            return redirect('/newpost')
        if len(body) < 10:
            flash("You can't tell a good story in under 10 characters!", "error")
            return redirect('/newpost')
        owner = User.query.filter_by(email=session['email']).first()
        owner_id = owner.id
        author = owner.username
        blog_entry = Blog(title, author, today, body, owner_id)
        db.session.add(blog_entry)
        db.session.commit()
        return redirect('/blog?blog-id='+str(blog_entry.id))

    return render_template('newpost.html', title="Add a Blog Entry", is_session=is_session())

@app.route('/login', methods=['POST', 'GET'])
def login():
    ##TODO: user without account clicks "Create Account" is directed to /signup
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_pw_hash(password, user.pw_hash):
            session['email'] = email
            flash("Logged in!", "success")
            return redirect('/newpost')
        else:
            ##TODO: enters username stored in db but incorrect password or incorrect username is redirected to login with appropriate error message
            flash("Error!", "error")
        
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(username, email,password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        elif existing_user:
            flash("Error! Existing User!", "error")
            return render_template('signup.html')
        else:
            ##TODO: user leaves any fields blank, enters username that already exists, mismatching passwords, too short a pass/username gets appropriate error messages
            flash("This doesn't make any sense", "error")
            return render_template('index.html')
    
    return render_template('signup.html')




@app.route('/logout', methods=['GET'])
def logout():
    if 'email' in session:
        del session['email']
        return redirect('/logout')
    return redirect('/')

if __name__ == "__main__":
    app.run()