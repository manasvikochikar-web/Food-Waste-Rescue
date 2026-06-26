from flask import Flask, request, redirect, render_template, url_for
import sqlite3

app = Flask(__name__)

# Function to initialize the database
def init_db():
    # Connect to (or create) the database file
    conn = sqlite3.connect('users.db')
    # Create the table if it doesn't exist
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users 
        (username TEXT, email TEXT, phone TEXT, password TEXT)
    ''')
    conn.commit()
    conn.close()

# Run the initialization
init_db()

# Route to serve the login page
@app.route('/')
def index():
    return render_template('index.html')

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



# 3. Server Execution (Must be at the very bottom)
if __name__ == '__main__':
    # 'debug=True' is essential for seeing server-side errors in your terminal
    app.run(debug=True, use_reloader=False, port=5000)