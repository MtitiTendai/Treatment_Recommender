from flask import Flask, render_template, url_for, flash
from flask import Flask, render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL 
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
from flask_wtf import FlaskForm

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydatabase'
app.secret_key = 'secrete_key'

mysql = MySQL(app)
class RegisterForm(FlaskForm):
    firstname = StringField('Firstame', validators= [DataRequired()])
    lastname = StringField('Lastname', validators= [DataRequired()])
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = StringField('Password', validators= [DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods= ['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']

        cur = mysql.connection.cursor()
        cur.execute("SELECT firstname, lastname, email, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            db_firstname, db_lastname, db_email, db_password = user
            db_fullname = db_firstname + " " + db_lastname

            if fullname != db_fullname:
                flash('Enter the correct fullname', 'danger')
                return redirect('/login')

            if password == db_password:
                flash('Login successful', 'success')
                session['email'] = email  # you can store session data if needed
                return redirect('/home')
            else:
                flash('Login failed, incorrect user email or password', 'danger')
                return redirect('/login')
        else:
            flash('User not found, please register to login', 'warning')
            return redirect('/signup')

    return render_template('login.html')    
    

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/home')
def home():
    return render_template("home.html")

# contact view funtion and path
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)",
                    (firstname, lastname, email, password))
        mysql.connection.commit()
        cur.close()

        flash('Registration successful! Please login.', 'success')
        return redirect('/login')

    return render_template("register.html", form = form)

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