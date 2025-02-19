from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Get the absolute path of users.txt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.txt")

# Function to load users from users.txt
def load_users():
    users = {}
    if not os.path.exists(USERS_FILE):  # Create file if it doesn't exist
        open(USERS_FILE, "w").close()
    with open(USERS_FILE, "r") as file:
        for line in file:
            if "," in line:  # Ensure line contains a comma
                try:
                    username, password = line.strip().split(",")
                    users[username] = password
                except ValueError:
                    print(f"Skipping malformed line: {line.strip()}")
    return users

# Function to save a new user
def save_user(username, password):
    with open(USERS_FILE, "a") as file:
        file.write(f"{username},{password}\n")

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    users = load_users()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid credentials!')
    return render_template('login.html', error=None)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users:
            return render_template('signup.html', error="Username already exists!")

        save_user(username, password)  # Save new user to users.txt
        return redirect('/login')

    return render_template('signup.html', error=None)

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', username=session['user'])
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
