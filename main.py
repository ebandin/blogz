from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz2:Blogz2password@localhost:8889/Blogz2'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class User(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref='owner')
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    blog = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __init__(self, title, blog, owner_id):
        self.title = title
        self.blog = blog
        self.owner_id = owner_id

@app.route('/', methods=['POST', 'GET'])
def index():
    #completed_title = Blog.query.all()
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        new_user = User(user, password)
        db.session.add(new_user)
        db.session.commit()

    user = session.get('username')
    if not session.get('logged_in'):
        return render_template('login.html')
    else: 
        return redirect('/homepage') 

@app.route('/homepage', methods=['POST', 'GET'])
def homepage():
    if request.method == 'POST':
        title = request.form['title']
        blog = request.form['blog']
        new_post = Blog(title, blog)
        db.session.add(new_post)
        db.session.commit()
    
    completed_title = Blog.query.all()

    return render_template('blog.html', completed_title = completed_title)

@app.route('/signup', methods=['POST', 'GET']) 
def signup(): 
    return render_template('signup.html')

@app.route('/blog', methods=['POST', 'GET']) 
def blog(): 

    completed_title = Blog.query.all()
    return render_template('blog.html')



@app.route('/newpost', methods=['POST', 'GET']) 
def postblog(): 
    if request.method == 'POST':
        title = request.form['title']
        blog = request.form['blog']
        new_post = Blog(title, blog)
        db.session.add(new_post)
        db.session.commit()
        
    return render_template('postblog.html')

@app.route('/blog-post', methods=['POST', 'GET']) 
def redirectblog(): 
    title = request.form['title']
    post = request.form['post']
    return render_template('blog-post.html', title = title, post = post)

@app.route('/login', methods=['POST'])
def login():
    error = ''
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        login = User.query.filter_by(username= user).first()
        if login == user:
            if login.password == password: 
                session['username'] = user
                return redirect('/newpost')
            else: 
                error = "you've entered the wrong password"
                return redirect('/login', error = error)
        else:
            error = "You have input an incorrect username"
            return redirect('/login', error = error)
    else: 
        return render_template('login.html') 
#@app.route('/index', methods=['POST', 'GET']) 
        #user = User.query.filter_by(email=email).first()
        #if user and user.password == password:
            #session['email'] = email
            #return redirect('/')
if __name__ == '__main__':
    app.run()