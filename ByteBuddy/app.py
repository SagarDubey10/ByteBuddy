from flask import Flask, request, jsonify, render_template, url_for, session, flash, redirect
from flask_session import Session
from difflib import get_close_matches
import json

app = Flask(__name__)
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
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").lower()
    knowledge_base = load_knowledge_base("knowledge_base.json")

    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base])

    if best_match:
        answer = get_answer(best_match, knowledge_base)
        return jsonify({"message": answer})
    else:
        return jsonify({"message": "I don't know the answer yet. Can you teach me?"})


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
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username and password are provided
        users = {
            "admin@123": {
                "password": "admin123"
            }
        }

        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('login'))

        # Check if username exists in the users dictionary
        if username in users:
            # Check if the provided password matches the stored password
            if password == users[username]["password"]:
                session['username'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('index'))  # Redirect to index page after login

        flash('Invalid username or password. Please try again.', 'error')
        return redirect(url_for('login'))

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


if __name__ == "__main__":
    app.run(debug=True)
