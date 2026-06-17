from flask import Flask, request, redirect, render_template, url_for

app = Flask(__name__)

# Serve the login page
@app.route('/')
def index():
    return render_template('index.html')

# Handle the form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    
    # Logic: Validate credentials here
    print(f"Login attempt: {username} | {email}")
    
    return redirect(url_for('main_page'))

# Serve the main page after login
@app.route('/main')
def main_page():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)