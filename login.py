from flask import Flask, render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__) 
app.secret_key = 'your_secret_key'

# MySQL Database Configuration
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'flask_coder' 
app.config['MYSQL_PASSWORD'] = '' 
app.config['MYSQL_DB'] = 'user_db'

mysql = MySQL(app)

@app.route('/') 
def home(): 
    return render_template('login.html')  # Login page template

@app.route('/login', methods=['GET', 'POST']) 
def login(): 
    if request.method == 'POST': 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor() 
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,)) 
        user = cursor.fetchone() 
        cursor.close()

        if user and check_password_hash(user[2], password):  # Assuming password is stored in column index 2
            session['user_id'] = user[0]  # Store user ID in session      
            session['username'] = user[1]
            return redirect(url_for('main'))  # Redirect to main page
    else:
        return "Invalid credentials. Try again."

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST']) 
def register(): 
    if request.method == 'POST': username = request.form['username'] 
    password = generate_password_hash(request.form['password'])  # Hash password for security cursor = mysql.connection.cursor() cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password)) mysql.connection.commit() cursor.close() return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/main') 
def main(): 
    if 'user_id' in session: return "Welcome, {}! This is the main page.".format(session['username']) 
    return redirect(url_for('login'))

@app.route('/logout') 
def logout(): 
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__': 
    app.run(debug=True)


