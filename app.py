from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "quiz_secret_key"

questions = [
    {
        "question": "What does HTML stand for?",
        "options": ["Hyper Text Markup Language", "High Tech Modern Language", "Hyper Transfer Markup Logic", "Home Tool Markup Language"],
        "answer": "Hyper Text Markup Language"
    },
    {
        "question": "Which HTTP method is used to send form data to the server?",
        "options": ["GET", "POST", "PUT", "DELETE"],
        "answer": "POST"
    },
    {
        "question": "What is Flask?",
        "options": ["A database", "A web framework for Python", "A JavaScript library", "A CSS framework"],
        "answer": "A web framework for Python"
    },
    {
        "question": "Which tag is used to link a CSS file in HTML?",
        "options": ["<style>", "<css>", "<link>", "<script>"],
        "answer": "<link>"
    },
    {
        "question": "What does CSS stand for?",
        "options": ["Creative Style Sheets", "Cascading Style Sheets", "Computer Style Syntax", "Colorful Style Sheets"],
        "answer": "Cascading Style Sheets"
    },
    {
        "question": "Which Python keyword is used to define a function?",
        "options": ["func", "define", "def", "fun"],
        "answer": "def"
    },
    {
        "question": "What does the render_template() function do in Flask?",
        "options": ["Runs JavaScript", "Renders an HTML template", "Connects to a database", "Sends an email"],
        "answer": "Renders an HTML template"
    }
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "GET":
        shuffled = random.sample(questions, len(questions))
        session["questions"] = shuffled
        session["current"] = 0
        session["score"] = 0
        session["total"] = len(shuffled)

    current = session.get("current", 0)
    total = session.get("total", len(questions))
    all_questions = session.get("questions", questions)

    if request.method == "POST":
        selected = request.form.get("answer")
        correct = all_questions[current]["answer"]
        if selected == correct:
            session["score"] += 1
        session["current"] = current + 1
        current = session["current"]

    if current >= total:
        return redirect(url_for("result"))

    q = all_questions[current]
    return render_template("quiz.html", question=q, number=current + 1, total=total)


@app.route("/result")
def result():
    score = session.get("score", 0)
    total = session.get("total", len(questions))

    if score == total:
        feedback = "Perfect score! You're amazing! 🎉"
    elif score >= total * 0.7:
        feedback = "Great job! You did really well! 👍"
    elif score >= total * 0.4:
        feedback = "Not bad! Keep practicing! 😊"
    else:
        feedback = "Don't worry, try again and you'll do better! 💪"

    return render_template("result.html", score=score, total=total, feedback=feedback)


@app.route("/restart")
def restart():
    session.clear()
    return redirect(url_for("quiz"))


if __name__ == "__main__":
    app.run(debug=True)
