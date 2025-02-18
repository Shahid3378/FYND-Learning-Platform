# from sqlalchemy import Column, Integer, String  # create_engine, 
# # from sqlalchemy.ext.declarative import declarative_Base
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin 
# from flask_bcrypt import Bcrypt
# from email_validator import validate_email, EmailNotValidError
# from sqlalchemy.orm import declarative_base, relationship, Column, Integer, String, ForeignKey

# Base = declarative_base()
# Base = SQLAlchemy()
# bcrypt = Bcrypt()


# # Data for Courses

# courses = {
#     1: {'title': 'HTML & CSS', 'description': 'Learn the fundamentals of web development with HTML and CSS.', 
#         'image': 'html_css_icon.jpeg',
#     'lessons': [
#         {'id': 1, 'title': 'Introduction to HTML & CSS', 'description': 'Learn the basics of HTML and CSS.'},
#         {'id': 2, 'title': 'CSS Basics', 'description': 'Learn how to style your web pages with CSS.'}
#     ]},
#     2: {'title': 'JavaScript', 'description': 'Dive into JavaScript for dynamic web content.', 
#     'image': 'js_icon.jpeg',
#     'lessons': [
#         {'id': 1, 'title': 'Introduction to JavaScript', 'description': 'Get started with JavaScript.'},
#         {'id': 2, 'title': 'JavaScript Functions', 'description': 'Learn about functions in JavaScript.'}
#     ]},
#     3: {'title': 'Python', 'description': 'Master Python programming.', 
#         'image': 'python_icon.jpeg',
#         'lessons': [
#         {'id': 1, 'title': 'Introduction to Python', 'description': 'Learn the basics of Python.'},
#         {'id': 2, 'title': 'Python Functions', 'description': 'Learn how to create functions in Python.'}
#     ]}
# }

# # Users model
# class Users(UserMixin, Base.Model):
#     __tablename__ = 'users'
#     id = Base.Column(Base.Integer, primary_key=True)
#     fname = Base.Column(Base.String(255), nullable=False)
#     lname = Base.Column(Base.String(255), nullable=False)
#     username = Base.Column(Base.String(255),unique=True, nullable=False, index=True)
#     email = Base.Column(Base.String(255),unique=True, nullable=False, index=True)
#     password = Base.Column(Base.String(255), nullable=False)
#     role =Base.Column(Base.String(255), default = 'user', nullable=False)

#     user_courses = Base.relationship('UserCourses', back_populates='user', lazy=True)
#     courses = Base.relationship('Courses', secondary='user_courses', back_populates='user') 

#     def __init__(self, fname, lname, username, email, password, role='user'):
#         self.fname = fname
#         self.lname = lname
#         self.username = username
#         self.email = email
#         self.role = role
#         self.password = bcrypt.generate_password_hash(password).decode('utf-8')

#     def check_password(self, password):
#         if len(password) < 8:  # Minimum length
#             return False
#         return bcrypt.check_password_hash(self.password, password)

# # UserCourses model
# class UserCourses(Base.Model):
    # __tablename__ = 'user_courses'
    # user_id = Base.Column(Base.Integer, Base.ForeignKey('users.id'), primary_key=True)
    # course_id = Base.Column(Base.Integer, Base.ForeignKey('courses.id'), primary_key=True)
    
    # user = Base.relationship('Users', back_populates='user_courses')
    # course = Base.relationship('Courses', back_populates='user_courses')

# Courses model
# class Courses(Base):
#     __tablename__ = 'courses'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(255), nullable=False)
#     description = Column(String(255), nullable=False)
#     image = Column(String(255), nullable=True)

    # user_courses = Base.relationship('UserCourses', back_populates='course', lazy=True)
    # users = Base.relationship('Users', secondary='user_courses', back_populates='courses')
    # lessons = Base.relationship('Lesson', backref='course', lazy=True)
    # quizzes = Base.relationship('Quizzes', backref='course', lazy=True)

# # Lesson model 
# class Lesson(Base.Model):
#     __tablename__ = 'lessons'
#     id = Base.Column(Base.Integer, primary_key=True)
#     title = Base.Column(Base.String(255), nullable=False)
#     # content = Base.Column(Base.String(255), nullable=False)
#     content = Base.Column(Base.Text, nullable=False)
#     course_id = Base.Column(Base.Integer, Base.ForeignKey('courses.id'), nullable=False)

#     user_progress = Base.relationship('UserLessonProgress', backref='lesson_progress', lazy=True)

# class UserLessonProgress(Base.Model):
#     __tablename__ = 'user_lesson_progress'
#     id = Base.Column(Base.Integer, primary_key=True)
#     user_id = Base.Column(Base.Integer, Base.ForeignKey('users.id'), nullable=False)
#     lesson_id = Base.Column(Base.Integer, Base.ForeignKey('lessons.id'), nullable=False)
#     lesson_completed = Base.Column(Base.Boolean, default=False)

#     # Many-to-one relationship with User
#     user = Base.relationship('Users', backref='lesson_progress')
#     lesson = Base.relationship('Lesson')

# # Quiz model 
# class Quizzes(Base.Model):
#     __tablename__ = 'quizzes'
#     id = Base.Column(Base.Integer, primary_key=True)
#     title = Base.Column(Base.String(255), nullable=False)
#     passing_score = Base.Column(Base.Integer, nullable=False, default=50)
#     course_id = Base.Column(Base.Integer, Base.ForeignKey('courses.id') , nullable=False)

#     quiz_questions = Base.relationship('Question', back_populates='quiz', lazy=True)

# class QuizResult(Base.Model):
#     __tablename__ = 'quiz_results'
#     id = Base.Column(Base.Integer, primary_key=True)
#     user_id = Base.Column(Base.Integer, Base.ForeignKey('users.id'), nullable=False)
#     quiz_id = Base.Column(Base.Integer, Base.ForeignKey('quizzes.id'), nullable=False)
#     passing_score = Base.Column(Base.Integer, nullable=False)

# class Question(Base.Model):
#     __tablename__ = 'questions'
#     id = Base.Column(Base.Integer, primary_key=True)
#     question = Base.Column(Base.String(255), nullable=False)
#     option_A = Base.Column(Base.String(255), nullable=False)
#     option_B = Base.Column(Base.String(255), nullable=False)
#     option_C = Base.Column(Base.String(255), nullable=False)
#     option_D = Base.Column(Base.String(255), nullable=False)
#     answer = Base.Column(Base.String(255), nullable=False)

#     quiz_id = Base.Column(Base.Integer, Base.ForeignKey('quizzes.id'), nullable=False)

#     quiz = Base.relationship('Quizzes', back_populates='quiz_questions')

# class Contact(Base.Model):
#     __tablename__ = 'contacts'
#     id = Base.Column(Base.Integer, primary_key=True)
#     name = Base.Column(Base.String(100), nullable=False)
#     email = Base.Column(Base.String(120), unique=True, nullable=False)
#     message = Base.Column(Base.Text, nullable=False)
    
#     def is_valid(self):
#         try:
#             validate_email(self.email)
#             return True
#         except EmailNotValidError as e:
#             raise ValueError(f"Invalid email: {self.email}. Error: {e}")

#     # def is_valid(self):
#     #     try:
#     #         validate_email(self.email)
#     #         return True
#     #     except EmailNotValidError:
#     #         return False

# # def init_data():
# #     # Create courses
# #     if not Courses.query.first():
# #         html_css_course = Courses(title="HTML & CSS", description="Learn the fundamentals of web development with HTML and CSS.")
# #         js_course = Courses(title="JavaScript", description="Dive into JavaScript for dynamic web content.")
# #         python_course = Courses(title="Python", description="Master Python programming.")
    
# #         Base.session.add_all([html_css_course, js_course, python_course])
# #         Base.session.commit()

# #         # Create lessons for HTML & CSS
# #         lesson1 = Lesson(title="Introduction to HTML & CSS", description="Learn the basics of HTML and CSS.", course_id=html_css_course.id)
# #         lesson2 = Lesson(title="CSS Basics", description="Learn how to style your web pages with CSS.", course_id=html_css_course.id)

# #         # Create lessons for JavaScript
# #         lesson3 = Lesson(title="Introduction to JavaScript", description="Get started with JavaScript.", course_id=js_course.id)
# #         lesson4 = Lesson(title="JavaScript Functions", description="Learn about functions in JavaScript.", course_id=js_course.id)

# #         # Create lessons for Python
# #         lesson5 = Lesson(title="Introduction to Python", description="Learn the basics of Python.", course_id=python_course.id)
# #         lesson6 = Lesson(title="Python Functions", description="Learn how to create functions in Python.", course_id=python_course.id)

# #         Base.session.add_all([lesson1, lesson2, lesson3, lesson4, lesson5, lesson6])
# #         Base.session.commit()

# #         # Create quizzes for HTML & CSS
# #         html_css_quiz = Quizzes(title="HTML & CSS Basics Quiz", passing_score=80, course_id=html_css_course.id)
# #         js_quiz = Quizzes(title="JavaScript Basics Quiz", passing_score=80, course_id=js_course.id)
# #         python_quiz = Quizzes(title="Python Basics Quiz", passing_score=80, course_id=python_course.id)

# #         Base.session.add_all([html_css_quiz, js_quiz, python_quiz])
# #         Base.session.commit()

# #         # Create questions for HTML & CSS quiz
# #         questions_html_css = [
# #             {"question": "What does HTML stand for?", 
# #             "option_A": "HyperText Markup Language", 
# #             "option_B": "Hyperlink Text Markup Language", 
# #             "option_C": "Home Tool Markup Language", 
# #             "option_D": "None of the above", 
# #             "answer": "HyperText Markup Language"
# #             },
#             {"question": "Which HTML element is used to define the title of a web page?",
#             "option_A": "<h1>", 
#             "option_B": "<title>", 
#             "option_C": "<head>", 
#             "option_D": "<body>", 
#             "answer": "<title>"
#             },
#             {"question": "Which of the following is the correct syntax for linking an external CSS file?", 
#             "option_A": "<style src='style.css'>", 
#             "option_B": "<link rel='stylesheet' href='style.css'>", "option_C": "<css src='style.css'>", 
#             "option_D": "<link href='style.css'>", 
#             "answer": "<link rel='stylesheet' href='style.css'>"
#             },
#             {"question": "How do you make a list in HTML?", 
#             "option_A": "<list>", 
#             "option_B": "<ul>", 
#             "option_C": "<ol>", 
#             "option_D": "<dl>", 
#             "answer": "<ul>"
#             },
#             {"question": "Which CSS property is used to change the background color of an element?", 
#             "option_A": "bgcolor", 
#             "option_B": "background-color", 
#             "option_C": "color", 
#             "option_D": "background", 
#             "answer": "background-color"
#             },
#             {"question": "Which tag is used to create a hyperlink in HTML?", 
#             "option_A": "<a>", 
#             "option_B": "<link>", 
#             "option_C": "<url>", 
#             "option_D": "<hyperlink>", 
#             "answer": "<a>"
#             },
#             {"question": "What is the correct syntax for adding a comment in CSS?", 
#             "option_A": "// comment", 
#             "option_B": "/* comment */", 
#             "option_C": "<!-- comment -->", 
#             "option_D": "# comment", 
#             "answer": "/* comment */"
#             },
#             {"question": "Which property is used to change the text color in CSS?", 
#             "option_A": "font-color", 
#             "option_B": "color", 
#             "option_C": "text-color", 
#             "option_D": "text-style", "answer": "color"
#             },
#             {"question": "What does the <div> tag represent in HTML?", "option_A": "A division or section in a document", "option_B": "A paragraph of text", 
#             "option_C": "An image container", 
#             "option_D": "A table row", 
#             "answer": "A division or section in a document"
#             },
#             {"question": "How do you add a background image in CSS?", "option_A": "background-image: url('image.jpg');", "option_B": "image: url('image.jpg');", "option_C": "background: 'image.jpg';", "option_D": "image-background: url('image.jpg');", 
#             "answer": "background-image: url('image.jpg');"
#             }
#         ]

#         # Create questions for JavaScript quiz
#         questions_js = [
#             {"question": "What is the correct way to define a variable in JavaScript?", 
#             "option_A": "var x = 5;", 
#             "option_B": "variable x = 5;", 
#             "option_C": "define x = 5;", 
#             "option_D": "x = 5;", 
#             "answer": "var x = 5;"
#             },
#             {"question": "Which method is used to display an alert box in JavaScript?", 
#             "option_A": "alert()", 
#             "option_B": "popup()", 
#             "option_C": "msg()", 
#             "option_D": "show()", 
#             "answer": "alert()"
#             },
#             {"question": "How do you create a function in JavaScript?", "option_A": "function myFunction() { }", 
#             "option_B": "func myFunction() { }", 
#             "option_C": "function: myFunction() { }", 
#             "option_D": "create function myFunction() { }", 
#             "answer": "function myFunction() { }"
#             },
#             {"question": "Which of the following is NOT a valid JavaScript data type?", 
#             "option_A": "Base.String", 
#             "option_B": "Base.Integer", 
#             "option_C": "Boolean", 
#             "option_D": "Undefined", 
#             "answer": "Base.Integer"
#             },
#             {"question": "How do you add a comment in JavaScript?", "option_A": "<!-- This is a comment -->", 
#             "option_B": "// This is a comment", 
#             "option_C": "/* This is a comment */", 
#             "option_D": "# This is a comment", 
#             "answer": "// This is a comment"
#             },
#             {"question": "What is the correct syntax to call a function named 'myFunction'?", "option_A": "call myFunction()", "option_B": "myFunction();", "option_C": "invoke myFunction()", "option_D": "execute myFunction()", "answer": "myFunction();"},
#             {"question": "Which of these is the correct way to declare an array in JavaScript?", 
#             "option_A": "let arr = [1, 2, 3];", 
#             "option_B": "let arr = (1, 2, 3);", 
#             "option_C": "let arr = {1, 2, 3};", 
#             "option_D": "let arr = 1, 2, 3;", 
#             "answer": "let arr = [1, 2, 3];"
#             },
#             {"question": "Which JavaScript method is used to find the length of an array?", 
#             "option_A": "length()", 
#             "option_B": "size()", 
#             "option_C": "arrayLength()", 
#             "option_D": ".length", 
#             "answer": ".length"
#             },
#             {"question": "Which of the following loops is used to execute a block of code while a condition is true?", "option_A": "for", 
#             "option_B": "while", 
#             "option_C": "do-while", 
#             "option_D": "All of the above", 
#             "answer": "All of the above"
#             },
#             {"question": "What is the result of '5' + 5 in JavaScript?", "option_A": "'55'", 
#             "option_B": "10", 
#             "option_C": "Error", 
#             "option_D": "'5' + '5'", 
#             "answer": "'55'"
#             }
#         ]

#         # Create questions for Python quiz
#         questions_python = [
#             {"question": "What is the correct syntax to print 'Hello, World!' in Python?", 
#             "option_A": "echo 'Hello, World!'", 
#             "option_B": "print('Hello, World!')", 
#             "option_C": "console.log('Hello, World!')", 
#             "option_D": "print(Hello, World!)", 
#             "answer": "print('Hello, World!')"
#             },
#             {"question": "Which of the following is a Python data type?", 
#             "option_A": "Base.Integer", 
#             "option_B": "Boolean", 
#             "option_C": "List", 
#             "option_D": "All of the above", 
#             "answer": "All of the above"
#             },
#             {"question": "How do you define a function in Python?", "option_A": "function myFunction():", 
#             "option_B": "def myFunction():", 
#             "option_C": "func myFunction():", 
#             "option_D": "function: myFunction()", 
#             "answer": "def myFunction():"
#             },
#             {"question": "Which of the following is the correct way to create a list in Python?", 
#             "option_A": "list = (1, 2, 3)", 
#             "option_B": "list = [1, 2, 3]", 
#             "option_C": "list = {1, 2, 3}", 
#             "option_D": "list = <1, 2, 3>", 
#             "answer": "list = [1, 2, 3]"
#             },
#             {"question": "How do you add an item to a list in Python?", "option_A": "list.add(4)", "option_B": "list.append(4)", "option_C": "list.insert(4)", "option_D": "list.push(4)", "answer": "list.append(4)"},
#             {"question": "Which of the following is used to handle errors in Python?", 
#             "option_A": "try...catch", 
#             "option_B": "try...except", 
#             "option_C": "catch...finally", 
#             "option_D": "throw...catch", 
#             "answer": "try...except"
#             },
#             {"question": "What is the result of '3 == 3' in Python?", "option_A": "True", 
#             "option_B": "False", 
#             "option_C": "Error", 
#             "option_D": "None", 
#             "answer": "True"
#             },
#             {"question": "Which Python operator is used for exponentiation?", 
#             "option_A": "^", 
#             "option_B": "**", 
#             "option_C": "*", 
#             "option_D": "++", 
#             "answer": "**"
#             },
#             {"question": "What is the correct syntax to comment a single line in Python?", 
#             "option_A": "<!-- This is a comment -->", 
#             "option_B": "# This is a comment", 
#             "option_C": "/* This is a comment */", 
#             "option_D": "// This is a comment", 
#             "answer": "# This is a comment"
#             },
#             {"question": "Which function is used to get the length of a list in Python?", "option_A": "list.size()", "option_B": "list.length()", "option_C": "len(list)", "option_D": "list.length", "answer": "len(list)"
#             }
#         ]

#         for q in questions_html_css:
#             Base.session.add(Question(**q, quiz_id=html_css_quiz.id))
        
#         for q in questions_js:
#             Base.session.add(Question(**q, quiz_id=js_quiz.id))
        
#         for q in questions_python:
#             Base.session.add(Question(**q, quiz_id=python_quiz.id))
        
#         Base.session.commit()

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime, LargeBinary
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

# User Model
class User(Base):
    _tablename_ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(String(100))
    password = Column(String(100), nullable=False)
    progress = relationship('UserProgress', back_populates='user', cascade="all, delete-orphan")
    enrollments = relationship('Enrollment', back_populates='user', cascade="all, delete-orphan")
    answers = relationship('UserAnswer', back_populates='user', cascade="all, delete-orphan")

# Course Model
class Course(Base):
    _tablename_ = 'courses'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    course_thumbnail = Column(LargeBinary, nullable=True)
    lessons = relationship('Lesson', back_populates='course', cascade="all, delete-orphan")
    quizzes = relationship('Quiz', back_populates='course', cascade="all, delete-orphan")
    progress = relationship('UserProgress', back_populates='course', cascade="all, delete-orphan")
    enrollments = relationship('Enrollment', back_populates='course', cascade="all, delete-orphan")