from flask import Flask, render_template, request, redirect
import sqlite3
import os 

app = Flask(__name__)

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

@app.route('/admin')
def admin():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM enrollments")
    students = cursor.fetchall()
    conn.close()
    return render_template('admin_dashboard.html', students=students)

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM enrollments WHERE id = ?", (id,))
    conn.commit()
    conn.close()
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
    
    return redirect('/')
  
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)