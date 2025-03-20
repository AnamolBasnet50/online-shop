from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
import os
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# Securely hash passwords
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS enrollments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT,
                        contact TEXT,
                        address TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        if username == ADMIN_USERNAME and hashed_password == ADMIN_PASSWORD_HASH:
            session['admin'] = True
            return redirect('/admin')
        else:
            flash("Invalid username or password!", "error")
            return redirect('/login')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash("Logged out successfully!", "success")
    return redirect('/login')

@app.route('/admin')
def admin():
    if 'admin' not in session:
        flash("Please log in first!", "warning")
        return redirect('/login')
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM enrollments")
    students = cursor.fetchall()
    conn.close()
    return render_template('admin_dashboard.html', students=students)

@app.route('/delete/<int:id>')
def delete_student(id):
    if 'admin' not in session:
        flash("Unauthorized action! Please log in.", "error")
        return redirect('/login')
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM enrollments WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Enrollment deleted successfully!", "success")
    return redirect('/admin')

@app.route('/enroll', methods=['POST'])
def enroll():
    name = request.form['name']
    email = request.form['email']
    contact = request.form['contact']
    address = request.form['address']
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO enrollments (name, email, contact, address) VALUES (?, ?, ?, ?)", 
                   (name, email, contact, address))
    conn.commit()
    conn.close()
    
    flash("Enrollment successful!", "success")
    return redirect('/')

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
