import sqlite3, os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "dev_secret_key"

# AUTH DB CONNECTION
def get_auth_db():
    conn = sqlite3.connect("auth.db")
    conn.row_factory = sqlite3.Row
    return conn

# TODO DB CONNECTION
def get_todo_db():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

# IMG DB CONNECTION
def get_img_db():
    conn = sqlite3.connect("img.db")
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

        conn = get_auth_db()
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

# GET ALL TASKS
@app.route('/get_tasks', methods = ['GET'])
def get_tasks():
    try:
        conn = get_todo_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks;")
        tasks = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(tasks)
    except sqlite3.Error as e:
        return jsonify({"Error": str(e)}), 500

# ADD NEW TASK
@app.route('/add_task', methods = ['POST'])
def add_task():
    data = request.get_json()
    task = data.get('task')
    category = data.get('category')
    due = data.get('due')
    remind = data.get('remind')

    if task and category:
        conn = get_todo_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task, category, due, remind) VALUES (?, ?, ?, ?)", (task, category, due, remind,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'})
    
    return jsonify({'status': 'error'})

# DELETE A TASK
@app.route('/delete_task', methods = ['POST'])
def delete_task():
    data = request.get_json()
    id = data.get('id')

    conn = get_todo_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({'status': 'deleted'})

# LOAD BLOGS PAGE
@app.route('/blogs')
def blogs():
    return render_template("blogs.html")

# ENSURE PROPER IMAGE FUNCTIONALITY
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# LOAD IMAGES PAGE
@app.route('/images')
def images():
    conn = get_img_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM images ORDER BY uploaded_at DESC;")
    images = cursor.fetchall()
    # If the above doesn't work, try the below
    # images = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return render_template("images.html", username = session['username'], images = images)

# UPLOAD AN IMAGE
@app.route('/upload', methods = ["POST"])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['image']

    if file.filename == "":
        return jsonify({'error':'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        subject = request.form.get('subject', '')
        topic = request.form.get('topic', '')

        conn = get_img_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO images (filename, subject, topic) VALUES (?, ?, ?)", (filename, subject, topic,))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Image uploaded successfully!'})
    
    return jsonify({'error':'Invalid file type'}), 400

# DOWNLOAD AN IMAGE
@app.route('/download/<int:image_id>')
def download_image(image_id):
    conn = get_img_db()
    cursor = conn.cursor()
    cursor.execute("SELECT filename FROM images WHERE id = ?", (image_id,))
    image = cursor.fetchone()
    conn.close()
    
    if not image:
        return "Image not found", 404
    
    filename = image['filename']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return "File not found", 404
    
    return send_file(filepath, as_attachment=True, download_name=filename)

# DELETE AN IMAGE
@app.route('/delete/<int:image_id>' , methods=['DELETE'])
def delete_image(image_id):
    conn = get_img_db()
    cursor = conn.cursor()

    # get filename
    cursor.execute("SELECT filename FROM images WHERE id = ?", (image_id,))
    image = cursor.fetchone()

    # if ts doesn't work, I might need something like the following line of code
    # tasks = [dict(row) for row in cursor.fetchall()]

    if not image:
        conn.close()
        return jsonify({'error':'Image not found'}), 404
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], image['filename'])

    # delete database entry
    cursor.execute("DELETE FROM images WHERE id = ?", (image_id,))
    conn.commit()
    conn.close()

    # delete file from folder
    if os.path.exists(filepath):
        os.remove(filepath)

    return jsonify({'message':'Image deleted successfully!'})

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

        conn = get_auth_db()
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