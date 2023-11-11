from flask import Flask , render_template , request
import mysql.connector 
from flask_bcrypt import Bcrypt
import re

app = Flask(__name__)
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/sign-up')
def signup():
    return render_template('signup.html')


@app.route('/post-signup' , methods = ['POST'])
def post_signup():
    user_email = request.form.get('email')
    password = request.form.get('pass')
    password_regex = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")
    email_regex = re.compile("^[A-Za-z0-9._]+@[A-Za-z]+\.[A-Za-z]{2,7}$")
    
    db = mysql.connector.connect(
        host="localhost", user = "afifa", password = "Forever" , database = "blogusers"
        )
    cursor = db.cursor()
    cursor.execute("SELECT email FROM users")
    users_list = cursor.fetchall()
    if user_email in [email[0] for email in users_list]:   # check availability of email
        return f"user already exists"   
      
    if not email_regex.match(user_email):   # check validity of email
        return "enter valid email"
        
    if not(password_regex.match(password)):  # chcekc strength of password
        return " enter Strong Password"   
    password =  bcrypt.generate_password_hash(password = password).decode('utf-8')
    cursor.execute("Insert into users (email , password) values (%s, %s);" , (user_email , password))
    db.commit()
    cursor.close()
    return f"""
           successfully regestred
    """
    
@app.route("/login")
def login():
    return render_template('login.html')
    
@app.route('/post-login', methods = ['POST'])
def post_login():
    user_email = request.form.get('email')
    password = request.form.get('pass')
    db = mysql.connector.connect(
        host="localhost", user = "afifa", password = "Forever", database = "blogusers"
        )
    cursor = db.cursor()
    cursor.execute("SELECT email FROM users")
    users_list = cursor.fetchall()
    if user_email in [email[0] for email in users_list]:    # check existence of user
        cursor.execute("SELECT password FROM users WHERE email = %s", (user_email , ))
        password_list = cursor.fetchall()
        cursor.close()
        if bcrypt.check_password_hash(password_list[0][0] , password):   # validate password
            return render_template('user.html')
        else:
            return f"wrong password"
    else:
        return f"user does not exist"
    
@app.route('/my_blogs' , methods = ['POST'])
def my_blogs():
    post = request.form.get('blog')
    print(post)
    return render_template('blogs.html', data = {"post" : post})

@app.route('/comments' , methods=['POST'])
def my_comments():
    comment = request.form.get('comment')
    post = request.form.get('blog')
    print(post)
    return render_template('blogs.html', 
            data = {
            "comment" : comment, 
            "post" : post
            } )
app.run(debug=True)