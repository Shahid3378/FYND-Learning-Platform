from BackEnd.app import db
from BackEnd.models2 import Quizzes, Question


def create_quizzes():
    # Check if quizzes already exist
    if not Quizzes.query.first():
        # Create quizzes for each course
        html_css_quiz = Quizzes(title="HTML & CSS Basics Quiz", passing_score=80, course_id=1)
        js_quiz = Quizzes(title="JavaScript Basics Quiz", passing_score=80, course_id=2)
        python_quiz = Quizzes(title="Python Basics Quiz", passing_score=80, course_id=3)

        db.session.add_all([html_css_quiz, js_quiz, python_quiz])
        db.session.commit()

        create_questions(html_css_quiz.id, js_quiz.id, python_quiz.id)


def create_questions(html_css_quiz_id, js_quiz_id, python_quiz_id):
    # Questions for HTML & CSS quiz
    questions_html_css = [
        {"question": "What does HTML stand for?",
        "option_A": "HyperText Markup Language",
        "option_B": "Hyperlink Text Markup Language",
        "option_C": "Home Tool Markup Language",
        "option_D": "None of the above",
        "answer": "HyperText Markup Language"},
        {"question": "Which HTML element is used to define the title of a web page?",
        "option_A": "<h1>",
        "option_B": "<title>",
        "option_C": "<head>",
        "option_D": "<body>",
        "answer": "<title>"},
        {"question": "Which of the following is the correct syntax for linking an external CSS file?",
        "option_A": "<style src='style.css'>",
        "option_B": "<link rel='stylesheet' href='style.css'>",
        "option_C": "<css src='style.css'>",
        "option_D": "<link href='style.css'>",
        "answer": "<link rel='stylesheet' href='style.css'>"}
    ]

    # Questions for JavaScript quiz
    questions_js = [
        {"question": "What is the correct way to define a variable in JavaScript?",
        "option_A": "var x = 5;",
        "option_B": "variable x = 5;",
        "option_C": "define x = 5;",
        "option_D": "x = 5;",
        "answer": "var x = 5;"},
        {"question": "Which method is used to display an alert box in JavaScript?",
        "option_A": "alert()",
        "option_B": "popup()",
        "option_C": "msg()",
        "option_D": "show()",
        "answer": "alert()"},
        {"question": "How do you create a function in JavaScript?",
        "option_A": "function myFunction() { }",
        "option_B": "func myFunction() { }",
        "option_C": "function: myFunction() { }",
        "option_D": "create function myFunction() { }",
        "answer": "function myFunction() { }"}
    ]

    # Questions for Python quiz
    questions_python = [
        {"question": "What is the correct syntax to print 'Hello, World!' in Python?",
        "option_A": "echo 'Hello, World!'",
        "option_B": "print('Hello, World!')",
        "option_C": "console.log('Hello, World!')",
        "option_D": "print(Hello, World!)",
        "answer": "print('Hello, World!')"},
        {"question": "Which of the following is a Python data type?",
        "option_A": "Integer",
        "option_B": "Boolean",
        "option_C": "List",
        "option_D": "All of the above",
        "answer": "All of the above"},
        {"question": "How do you define a function in Python?",
        "option_A": "function myFunction():",
        "option_B": "def myFunction():",
        "option_C": "func myFunction():",
        "option_D": "function: myFunction()",
        "answer": "def myFunction():"}
    ]

    # Add questions to the database
    for q in questions_html_css:
        db.session.add(Question(**q, quiz_id=html_css_quiz_id))
    for q in questions_js:
        db.session.add(Question(**q, quiz_id=js_quiz_id))
    for q in questions_python:
        db.session.add(Question(**q, quiz_id=python_quiz_id))

    db.session.commit()


if __name__ == "__main__":
    create_quizzes()
