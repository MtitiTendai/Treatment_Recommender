from flask import Flask, render_template, url_for
from flask import Flask, render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL 
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydatabase'
app.secret_key = 'your_secrete_key_here'

mysql = MySQL(app)
class RegisterForm():
    firstname = StringField('Firstame', validators= [DataRequired()])
    lastname = StringField('Lastname', validators= [DataRequired()])
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = StringField('Password', validators= [DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/home')
def home():
    return render_template("home.html")

# contact view funtion and path
@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# developer view funtion and path
@app.route('/developer')
def developer():
    return render_template("developer.html")

# about view funtion and path
@app.route('/blog')
def blog():
    return render_template("blog.html")
    

if __name__ == '__main__':
    app.run(debug= True)