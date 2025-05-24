from flask import Flask, request, jsonify, render_template, url_for, session, flash, redirect
from flask_session import Session
from difflib import get_close_matches
from datetime import datetime
import pytz
import json
import sqlite3
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)


def load_knowledge_base(file_path: str) -> list:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading knowledge base: {e}")
        return []


def save_knowledge_base(file_path: str, data: list) -> None:
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: list) -> str | None:
    matches = get_close_matches(user_question.lower(), questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer(user_question: str, knowledge_base: list) -> str | None:
    for entry in knowledge_base:
        if entry["question"].lower() == user_question.lower():
            return entry["answer"]
    return None


@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").lower()
    knowledge_base = load_knowledge_base("knowledge_base.json")

    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base])

    if best_match:
        answer = get_answer(best_match, knowledge_base)
    else:
        answer = "I don't know the answer yet. Can you teach me?"

    # Save chat to DB
    save_conversation(session.get("username"), user_input, answer)

    return jsonify({"message": answer})



@app.route('/learn', methods=['POST'])
def learn():
    data = request.get_json()
    question = data.get("question", "").lower()
    answer = data.get("answer", "").lower()

    knowledge_base = load_knowledge_base("knowledge_base.json")
    knowledge_base.append({"question": question, "answer": answer})
    save_knowledge_base("knowledge_base.json", knowledge_base)

    return jsonify({"status": "success"})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('byte_buddy.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect('/dashboard')  # or wherever your home/chat page is
        else:
            return "Invalid credentials. Please try again."

    return render_template('login.html')



@app.route('/logout')
def logout():
    # Clear session data
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/help')
def help():
     print("Rendering help.html")  # Debug output
     return render_template('help.html')

def save_conversation(username, message, response):
    try:
        ist = pytz.timezone('Asia/Kolkata')  # 👈 India timezone
        now_ist = datetime.now(ist)
        formatted_time = now_ist.strftime("%b %d, %Y - %I:%M %p")  # 👈 Apr 19, 2025 - 07:06 PM

        with sqlite3.connect('byte_buddy.db') as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO conversations (username, message, response, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (username, message, response, formatted_time))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

@app.route('/history')
def history():
    username = session.get("username")
    conn = sqlite3.connect('byte_buddy.db')
    c = conn.cursor()
    c.execute('''
        SELECT DATE(timestamp), message, response, timestamp
        FROM conversations
        WHERE username = ?
        ORDER BY timestamp DESC
    ''', (username,))
    chats = c.fetchall()
    conn.close()
    return render_template('history.html', chats=chats)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # You can hash this too

        conn = sqlite3.connect('byte_buddy.db')
        c = conn.cursor()

        # Check if user already exists
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        if c.fetchone():
            return "User already exists. Try logging in."

        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('chat.html')


if __name__ == "__main__":
    app.run(debug=True)