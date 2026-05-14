import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "dev_secret_key"

# AUTH DB CONNECTION
def get_db():
    conn = sqlite3.connect("auth.db")
    conn.row_factory = sqlite3.Row
    return conn

# LOAD LOGIN PAGE
@app.route('/')
def home():
    return redirect(url_for('login'))

# LOGIN ROUTING
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM users WHERE email = ? AND password = ?""", (email, password))
        user = cursor.fetchone()

        if user:
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password!")
        conn.close()

    return render_template("login.html")

# DASHBOARD ROUTING
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username = session['username'])
    return redirect(url_for('login'))

# LOAD TASKS PAGE
@app.route('/tasks')
def tasks():
    return render_template("tasks.html", username = session['username'])

# LOAD BLOGS PAGE
@app.route('/blogs')
def blogs():
    return render_template("blogs.html")

# LOAD IMAGES PAGE
@app.route('/images')
def images():
    return render_template("images.html", username = session['username'])

# LOGOUT ROUTING
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# SIGNUP ROUTING
@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute("""INSERT INTO users (username, email, password) VALUES (?,?,?)""", (username, email, password))
            conn.commit()
            flash("Account created successfully!")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists!')
        finally:
            conn.close()

    return render_template('signup.html')

# RUN APP
if __name__ == '__main__':
    app.run(debug=True)