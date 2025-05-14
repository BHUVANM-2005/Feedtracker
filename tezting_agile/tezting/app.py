from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'

# Database setup
def init_db():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    
    # Feedback table
    c.execute('''CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        professor TEXT,
        rating INTEGER,
        comment TEXT
    )''')

    # Admin table
    c.execute('''CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )''')

    # Add default admin if not exists
       # Add only SIDDARTHK as admin if not exists
    c.execute("SELECT * FROM admin WHERE username = 'SIDDARTHK'")
    if not c.fetchone():
        c.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ('SIDDARTH', '12345'))

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def select_login():
    return render_template('select_login.html')

@app.route('/student_login')
def student_login():
    return render_template('login.html')

@app.route('/submit/classroom', methods=['POST'])
def submit_classroom():
    username = session.get('username')
    room = request.form['room']
    issue = request.form['issue']

    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('INSERT INTO feedback (username, professor, rating, comment) VALUES (?, ?, ?, ?)',
              (username, 'Classroom Issue: ' + room, None, issue))
    conn.commit()
    conn.close()
    return render_template('success.html')

@app.route('/submit/lab', methods=['POST'])
def submit_lab():
    username = session.get('username')
    lab = request.form['lab']
    issue = request.form['issue']

    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('INSERT INTO feedback (username, professor, rating, comment) VALUES (?, ?, ?, ?)',
              (username, 'Lab Issue: ' + lab, None, issue))
    conn.commit()
    conn.close()
    return render_template('success.html')

@app.route('/submit/other', methods=['POST'])
def submit_other():
    username = session.get('username')
    issue_type = request.form['type']
    issue = request.form['issue']

    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('INSERT INTO feedback (username, professor, rating, comment) VALUES (?, ?, ?, ?)',
              (username, 'Other Issue: ' + issue_type, None, issue))
    conn.commit()
    conn.close()
    return render_template('success.html')

@app.route('/login', methods=['POST'])
def do_login():
    session['username'] = request.form['username']
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/report/classroom')
def report_classroom():
    return render_template('report_classroom.html')

@app.route('/report/lab')
def report_lab():
    return render_template('report_lab.html')

@app.route('/report/other')
def report_other():
    return render_template('report_other.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    username = session.get('username')
    professor = request.form['professor']
    rating = request.form['rating']
    comment = request.form['comment']

    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('INSERT INTO feedback (username, professor, rating, comment) VALUES (?, ?, ?, ?)',
              (username, professor, rating, comment))
    conn.commit()
    conn.close()
    return render_template('success.html')

@app.route('/admin')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin_login', methods=['POST'])
def handle_admin_login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, password))
    admin = c.fetchone()

    if admin:
        c.execute('SELECT * FROM feedback')
        all_feedback = c.fetchall()
        conn.close()
        return render_template('admin_dashboard.html', feedbacks=all_feedback)
    else:
        conn.close()
        return "Invalid admin credentials"

if __name__ == '__main__':
    app.run(debug=True)
