import os
import requests
from flask import Flask, render_template, request, jsonify, session, redirect
from dotenv import load_dotenv
#import openai
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to your desired secret key

load_dotenv()  # Load environment variables from .env file

# Access your API key
openai_api_key = os.getenv('API_KEY')

API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

# SQLite3 Database Initialization
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)")
conn.commit()

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            session['username'] = username
            return redirect('/')
        else:
            return render_template('login.html', error=True)
    return render_template('login.html', error=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if create_user(username, password):
            session['username'] = username
            return redirect('/')
        else:
            return render_template('register.html', error=True)
    return render_template('register.html', error=False)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/chat', methods=['POST'])
def chat():
    if 'username' not in session:
        return jsonify({'message': 'You need to be logged in to use the chatbot.'})
    message = request.form['message']
    response = query_chatbot(message)
    return jsonify({'message': response})

def create_user(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user and user[2] == password:
        return True
    return False

def query_chatbot(message):
    api_key = os.getenv('API_KEY')  # Get the API key from the environment variable
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                     {'role': 'user', 'content': message}]
    }
    response = requests.post(API_ENDPOINT, json=data, headers=headers)
    response_json = response.json()
    return response_json['choices'][0]['message']['content']

if __name__ == '__main__':
    app.run()
