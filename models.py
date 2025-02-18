from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, LargeBinary
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

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

# User Model
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    fname = Column(String(100), nullable=False)
    lname = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(String(100))
    password = Column(String(100), nullable=False)
    # progress = relationship('UserProgress', back_populates='user', cascade="all, delete-orphan")
    enrollments = relationship('Enrollment', back_populates='user', cascade="all, delete-orphan")
    # answers = relationship('UserAnswer', back_populates='user', cascade="all, delete-orphan")

# Course Model
class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    course_thumbnail = Column(String(100), nullable=True)
    image = Column(String(100), default='logo.jpg')

    # Relationship with Lesson
    lessons = relationship('Lesson', back_populates='course', cascade="all, delete-orphan")
    quizzes = relationship('Quiz', back_populates='course', cascade="all, delete-orphan")
    enrollments = relationship('Enrollment', back_populates='course', cascade="all, delete-orphan")

class Enrollment(Base):
    __tablename__ = 'enrollments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)

    # Relationship with User and Course
    user = relationship('Users', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')

# Lesson Model
class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(200), nullable=False)
    completed = Column(Boolean, default=False)
    course_link = Column(String(500), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'))

    # Relationship with Course
    course = relationship('Course', back_populates='lessons')

# Quiz Model
class Quiz(Base):
    __tablename__ = 'quizzes'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    passing_score = Column(Integer, nullable=False, default=50)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)

    # Relationship with Course and Questions
    course = relationship('Course', back_populates='quizzes')
    quiz_questions = relationship('Question', back_populates='quiz', lazy=True)

# QuizResult Model
class QuizResult(Base):
    __tablename__ = 'quiz_results'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=True)
    passing_score = Column(Integer, nullable=False)

    # Relationship with User and Quiz
    user = relationship('Users', backref='quiz_results')
    quiz = relationship('Quiz', backref='quiz_results')

# Question Model
class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question = Column(String(255), nullable=False)
    option_A = Column(String(255), nullable=False)
    option_B = Column(String(255), nullable=False)
    option_C = Column(String(255), nullable=False)
    option_D = Column(String(255), nullable=False)
    answer = Column(String(255), nullable=False)

    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)

    # Relationship with Quiz
    quiz = relationship('Quiz', back_populates='quiz_questions')

# Contact Model
class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    message = Column(String(255), nullable=False)
