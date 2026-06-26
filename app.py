from flask import Flask, request, redirect, render_template, url_for
import sqlite3
import os

app = Flask(__name__)

# 1. Database Setup
def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users 
        (username TEXT, email TEXT, phone TEXT, password TEXT)
    ''')
    conn.commit()
    conn.close()

# Initialize the database immediately
init_db()

# 2. Routes (Must be defined BEFORE app.run)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # Capture form data
    username = request.form.get('username')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    
    # Save to database
    conn = sqlite3.connect('users.db')
    conn.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (username, email, phone, password))
    conn.commit()
    conn.close()
    
    # Redirect to the main_page route
    return redirect(url_for('main_page'))

@app.route('/main')
def main_page():
    # Ensure 'main.html' exists in the /templates folder
    return render_template('main.html')


@app.route('/donate.html')
def donate():
    return render_template('donate.html')


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')  


# 3. Server Execution (Configured for Railway)
if __name__ == '__main__':
    # Railway provides a dynamic port via environment variables.
    # We default to 5000 if running locally.
    port = int(os.environ.get("PORT", 5000))
    
    # Crucial: host must be '0.0.0.0' for Railway to route traffic to your app
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
