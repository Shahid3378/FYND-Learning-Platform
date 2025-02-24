from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
from werkzeug.utils import secure_filename #type: ignore
from io import BytesIO
from werkzeug.security import generate_password_hash, check_password_hash   # type: ignore
from database import session as db_session
from models import Course, Users, Lesson,Question,Quiz, QuizResult, Contact, Enrollment
import json
from sqlalchemy.orm import joinedload
from datetime import datetime

app = Flask(__name__,
            template_folder='templates', 
            static_folder='static')
app.config['SECRET_KEY'] = '9224ab35a0fb246961b5d55a' 

admin = db_session.query(Users).filter_by(username="Shahid").first()
if not admin:
    db_session.add(Users(
        fname="Shahid",
        lname="Raja",
        username="Shahid",
        email="admin@gmail.com",
        password=generate_password_hash("Flask@123"),
        role="admin"
    ))
    db_session.commit()
    print("✅ Admin user created successfully!")

user = db_session.query(Users).filter_by(username="user1").first()
if not user:
    db_session.add(Users(
        fname="User",
        lname="1",
        username="user1",
        email="user1@gmail.com",
        password=generate_password_hash("User1@123"),
        role="user"
    ))
    db_session.commit()
    print("✅ Default user created successfully!")

#------------------------------------------------------------------------

# Admin: Shahid
# Password: Flask@123
# Hashed Password: scrypt:32768:8:1$NhkbRj8G4Zu6V127$a081d67ce50b2d476c7555763d0d64725126d47b272d336ba7fd02a064344f058f072d6aaf124c0edbfc5a5cdca989a3e2dbdd59f50e31b3b714a799089ff14e

#------------------------------------------------------------------------



@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home/')
def home():
    username = session.get('username')
    role = session.get('role')

    courses = db_session.query(Course).all()

    # Log courses data before passing it to the template
    print(f"Courses before encoding: {courses}")

    for course in courses:
        if course.course_thumbnail:
            course.course_thumbnail = course.course_thumbnail
        else:
            course.course_thumbnail = None

    # courses = db_session.query(Course).all()
    return render_template('home.html', courses=courses)


@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db_session.query(Users).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # login_user(user)
            session['username'] = username
            session['role'] = user.role

            flash("Login successful!", "success")

            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for('login'))
        
    return render_template('login.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')

        if password != password_confirmation:
            flash("Passwords do not match", "error")
            return redirect(url_for('register'))
        
        existing_user = db_session.query(Users).filter_by(username=username).first()

        if existing_user:
            flash("Username or email already exists", "error")
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)

        new_user = Users(
                fname=fname, 
                lname=lname, 
                username=username, 
                email=email, 
                password=hashed_password, 
                role="user"
            )

        # new_user = Users(fname=fname, lname=lname,username=username, email=email, password=password_confirmation, role="user")

        # user = Users(username=username, email=email, password=password)
        db_session.add(new_user)
        db_session.commit()

        flash("User Registration Successful! ")
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/courses/')
def course_list():
    courses = db_session.query(Course).all()
    # print(courses)
    return render_template('courses.html', courses=courses)

@app.route('/enroll/<int:course_id>', methods=['POST'])
def enroll_in_course(course_id):
    if 'username' not in session:
        flash("You must be logged in to enroll in a course.", "warning")
        return redirect(url_for('login'))

    # Fetch course and user
    course = db_session.query(Course).get(course_id)
    user = db_session.query(Users).filter_by(username=session['username']).first()

    if not course:
        flash("Course not found!", "danger")
        return redirect(url_for('course_list'))
    
    if not user:
        flash("User not found!", "danger")
        return redirect(url_for('login'))

    # Check if user is already enrolled
    existing_enrollment = db_session.query(Enrollment).filter_by(user_id=user.id, course_id=course.id).first()

    if existing_enrollment:
        flash("You are already enrolled in this course.", "info")
    else:
        # Enroll the user
        enrollment = Enrollment(user_id=user.id, course_id=course.id)
        db_session.add(enrollment)
        db_session.commit()
        flash(f"Successfully enrolled in {course.title}!", "success")

    return redirect(url_for('course_content', course_id=course.id))

@app.route('/course/<int:course_id>/')
def course_content(course_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    course = db_session.query(Course).get(course_id)
    if not course:
        flash("Course not found!", "error")
        return redirect(url_for('course_list'))
    
    user = db_session.query(Users).filter_by(username=session['username']).first()
    if not user:
            flash("User not found!", "error")
            return redirect(url_for('login'))

    is_enrolled = db_session.query(Enrollment).filter_by(user_id=user.id, course_id=course.id).first() is not None
    if not is_enrolled:
        flash("You need to enroll in this course to access lessons.", "warning")
        # return redirect(url_for('course_list'))

    return render_template('course_content.html', course=course, is_enrolled=is_enrolled)

@app.route('/course/<int:course_id>/lesson/<int:lesson_id>/')
def course_lesson(course_id, lesson_id):
    course = db_session.query(Course).get(course_id)
    lesson = db_session.query(Lesson).get(lesson_id)

    if not course:
        flash("Course not found!", "error")
        return redirect(url_for('course_list'))

    if not lesson:
        flash("Lesson not found!", "error")
        return redirect(url_for('course_content', course_id=course_id))

    return render_template('course_lesson.html', course=course, lesson=lesson, course_id=course_id)


@app.route('/course/<int:course_id>/quiz/')
def course_quiz(course_id):
    course = db_session.query(Course).options(joinedload(Course.quizzes).joinedload(Quiz.quiz_questions)).filter_by(id=course_id).first()

    if not course:
        flash('Course not found!', 'danger')
        return redirect(url_for('course_list'))
    
    print("Course:", course.title)
    for quiz in course.quizzes:
        print("Quiz:", quiz.title)
        for question in quiz.quiz_questions:
            print("Question:", question.question)

    return render_template('quiz.html', course=course)


@app.route('/course/<int:course_id>/lesson/<int:lesson_id>/quiz/', methods=['GET', 'POST'])
def submit_quiz(course_id, lesson_id):
    if 'username' not in session:
        flash('You must be logged in to attempt quizzes.', 'error')
        return redirect(url_for('login'))

    course = db_session.query(Course).get(course_id)
    lesson = db_session.query(Lesson).get(lesson_id)
    user = db_session.query(Users).filter_by(username=session['username']).first()

    if not course or not lesson or not user:
        flash("Course, lesson or user not found!", "error")
        return redirect(url_for('course_list'))
    
    if request.method == 'POST':
        score = 0
        total_questions = 0 #len(course.quizzes)

        for quiz in course.quizzes:
            for question in quiz.quiz_questions:
                selected_answer = request.form.get(f'answer_{question.id}')
                print(f"Selected: {selected_answer}, Correct: {question.answer}")

                if selected_answer == question.answer:
                    score += 1
                total_questions += 1

            existing_result = db_session.query(QuizResult).filter_by(user_id=user.id, quiz_id=quiz.id).first()

            if existing_result:
                # Update the existing result
                existing_result.passing_score = score
                existing_result.total_questions = total_questions
            else:
                quiz_result = QuizResult(
                    user_id=user.id, 
                    quiz_id=quiz.id, 
                    passing_score=score,
                    total_questions=total_questions
                )
                db_session.add(quiz_result)
        
        db_session.commit()

        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        flash(f'You scored {score}/{total_questions} ({percentage:.2f}%)', 'success')

        return redirect(url_for('user_dashboard', course=course, lesson=lesson))

    return render_template('quiz.html', course=course, lesson=lesson)


@app.route('/user_courses/')
def user_courses():
    user = db_session.query(Users).get(1)
    if user:
        courses = user.course  # Access the courses the user is enrolled in
        return render_template('user_courses.html', user=user, courses=courses)
    return "User not found", 404


@app.route('/certificate/<int:user_id>/<int:course_id>')
def certificate(user_id, course_id):
    user = db_session.query(Users).get(user_id)
    course = db_session.query(Course).get(course_id)
    # instructor_name = "Your Instructor's Name"
    completion_date = datetime.now()
    instructor_name = "Shahid Raja"

    if not user or not course:
        flash("User or Course not found.", "danger")
        return redirect(url_for('course_list'))

    return render_template(
        'certificate.html',
        user=user,
        course=course,
        instructor_name=instructor_name,
        completion_date=completion_date
    )


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    # if  current_user.is_authenticated:
    # user = db_session.get(Users)

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            flash("Please fill out all fields!", "error")
            return redirect(url_for('contact'))
        
        new_contact = Contact(name=name, email=email, message=message)
        db_session.add(new_contact)
        db_session.commit()

        flash("Message sent successfully!", "success")
        return redirect(url_for('contact'))
    
    return render_template('contact.html')


#  Admin routes

# Route to manage users
@app.route('/admin/manage_users/')
def admin_manage_users():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    users = db_session.query(Users).options(joinedload(Users.enrollments).joinedload(Enrollment.course)).all()
    return render_template('admin_manage_users.html', users=users)

# Route to add a new user
# For Adding User
@app.route('/admin/add_user/', methods=['GET', 'POST'])
def admin_add_user():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    courses = db_session.query(Course).all()

    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        enrolled_courses = request.form.getlist('enrolled_courses[]')

        hashed_password = generate_password_hash(password)

        existing_user = db_session.query(Users).filter_by(username=username).first()
        if existing_user:
            flash("User already exists!", "error")
            return redirect(url_for('admin_add_user'))
        
        new_user = Users(
            fname=fname,
            lname=lname,
            username=username,
            email=email,
            password=hashed_password,
            role=role
        )

        db_session.add(new_user)
        db_session.commit()

        # Enroll user in selected courses
        for course_id in enrolled_courses:
            enrollment = Enrollment(user_id=new_user.id, course_id=int(course_id))
            db_session.add(enrollment)

        db_session.commit()

        flash("User added successfully with enrolled courses!", "success")
        return redirect(url_for('admin_manage_users'))
    
    return render_template('admin_add_user.html', courses=courses)


# For Editing User
@app.route('/admin/edit_user/<int:user_id>/', methods=['GET', 'POST'])
def admin_edit_user(user_id):
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    user = db_session.query(Users).get(user_id)
    courses = db_session.query(Course).all()
    user_enrollments = [enrollment.course_id for enrollment in db_session.query(Enrollment).filter_by(user_id=user.id).all()]

    if not user:
        flash("User not found!", "error")
        return redirect(url_for('admin_manage_users'))
    
    if request.method == 'POST':
        # Update user info
        user.fname = request.form.get('fname')
        user.lname = request.form.get('lname')
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        if request.form['password']:
            user.password = generate_password_hash(request.form['password'])
        user.role = request.form.get('role')

        # Handle Course Enrollment Updates
        selected_courses = list(map(int, request.form.getlist('enrolled_courses[]')))
        current_enrollments = set(user_enrollments)

        # Add new enrollments
        for course_id in set(selected_courses) - current_enrollments:
            db_session.add(Enrollment(user_id=user.id, course_id=course_id))

        # Remove unchecked enrollments
        for course_id in current_enrollments - set(selected_courses):
            db_session.query(Enrollment).filter_by(user_id=user.id, course_id=course_id).delete()

        db_session.commit()
        flash("User updated successfully, including course enrollments!", "success")
        return redirect(url_for('admin_manage_users'))
    
    return render_template(
        'admin_edit_user.html', 
        user=user, 
        courses=courses, 
        user_enrolled_course_ids=user_enrollments
    )

# Route to delete a user
@app.route('/admin/delete_user/<int:user_id>/', methods=['POST'])
def admin_delete_user(user_id):
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    user = db_session.query(Users).get(user_id)

    if not user:
        flash("User not found!", "danger")
        return redirect(url_for('admin_manage_users'))

    if request.method == 'POST':
        db_session.delete(user)
        db_session.commit()
        flash("User deleted successfully!", "success")
        return redirect(url_for('admin_manage_users'))

    # Render confirmation page
    return render_template('admin_delete_user.html', user=user)

# Route to confirm user deletion
@app.route('/admin/delete_user/<int:user_id>/', methods=['GET', 'POST'])
def admin_delete_user_page(user_id):
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    # Fetch user data to confirm deletion
    user = db_session.query(Users).get(user_id)
    
    if not user:
        flash("User not found!", "error")
        return redirect(url_for('admin_manage_users'))
    
    if request.method == 'POST':
        # Perform deletion
        db_session.delete(user)
        db_session.commit()
        flash("User deleted successfully!", "success")
        return redirect(url_for('admin_manage_users'))

    # Render confirmation page on GET
    return render_template('admin_delete_user.html', user=user)

@app.route('/admin/user_progress/<int:user_id>')
def admin_user_progress(user_id):
    user = db_session.query(Users).filter_by(id=user_id).first()
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('admin_manage_users'))

    enrollments = db_session.query(Enrollment).filter_by(user_id=user_id).all()
    quiz_results = db_session.query(QuizResult).filter_by(user_id=user_id).all()

    return render_template('admin_user_progress.html', user=user, enrollments=enrollments, quiz_results=quiz_results)

# -------------------------------------------------------------------------

# Route to manage courses
@app.route('/admin/manage_courses/')
def admin_manage_courses():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    courses = db_session.query(Course).all()
    return render_template('admin_manage_courses.html', courses=courses)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin/add_course/', methods=['POST', 'GET'])
def admin_add_course():
    if 'username' not in session or session.get('role') != 'admin':
        flash("Access Denied! Admins only.", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            course_thumbnail = None

            if 'course_thumbnail' in request.files:
                file = request.files['course_thumbnail']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join('static/img', filename))
                    course_thumbnail = filename

            new_course = Course(title=title,
                                description=description, course_thumbnail=course_thumbnail
                                )
            db_session.add(new_course)
            db_session.flush()

            # Adding Lessons
            lesson_titles = request.form.getlist('lesson_title[]')
            lesson_contents = request.form.getlist('lesson_content[]')
            lesson_links = request.form.getlist('lesson_link[]')

            for i in range(len(lesson_titles)):
                new_lesson = Lesson(title=lesson_titles[i],
                                    content=lesson_contents[i], 
                                    course_link=lesson_links[i], course_id=new_course.id
                                    )
                db_session.add(new_lesson)

            new_quiz = Quiz(title=f"Quiz for {new_course.title}", course_id=new_course.id)
            db_session.add(new_quiz)
            db_session.flush()

            # Adding Quizzes
            quiz_questions = request.form.getlist('quiz_question[]')
            options_A = request.form.getlist('option_A[]')
            options_B = request.form.getlist('option_B[]')
            options_C = request.form.getlist('option_C[]')
            options_D = request.form.getlist('option_D[]')
            correct_answers = request.form.getlist('correct_answer[]')

            for i in range(len(quiz_questions)):
                new_question = Question(question=quiz_questions[i],
                                    option_A=options_A[i], option_B=options_B[i], option_C=options_C[i], option_D=options_D[i], answer=correct_answers[i], quiz_id=new_quiz.id
                                    )
                db_session.add(new_question)

            db_session.commit()
            flash("Course, lessons, and quizzes added successfully!", "success")
            return redirect(url_for('admin_manage_courses'))
        except Exception as e:
            db_session.rollback()
            flash(f"Error adding course: {e}", "error")

    return render_template('admin_add_course.html')


# Route to delete a course
@app.route('/admin/delete_course/<int:course_id>/', methods=['POST'])
def admin_delete_course(course_id):
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    course_to_delete = db_session.query(Course).get(course_id)

    if not course_to_delete:
        flash("Course not found!", "error")
        return redirect(url_for('admin_manage_courses'))
    
    try:
        db_session.delete(course_to_delete)
        db_session.commit()
        flash("Course and lessons deleted successfully!", "success")
    except Exception as e:
        db_session.rollback()
        flash(f"Error deleting course: {e}", "error")
    return redirect(url_for('admin_manage_courses'))


# Route to delete lesson details
@app.route('/admin/delete_lesson/<int:lesson_id>/', methods=['POST'])
def admin_delete_lesson(lesson_id):
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    lesson_to_delete = db_session.query(Lesson).get(lesson_id)

    if not lesson_to_delete:
        flash("Lesson not found!", "error")
        return redirect(url_for('admin_edit_course', course_id=lesson_to_delete.course_id))

    # Deleting the lesson
    # if request.method == 'POST':
    db_session.delete(lesson_to_delete)
    db_session.commit()
    flash("Lesson deleted successfully!", "success")
    # else:
        # flash("Lesson not found!", "error")

    return redirect(url_for('admin_edit_course', course_id=lesson_to_delete.course_id))

# Route to update course details
@app.route('/admin/update_course/<int:course_id>/', methods=['GET', 'POST'])
def admin_update_course(course_id):
    if 'username' not in session or session.get('role') != 'admin':
        flash("Access Denied! Admins only.", "danger")
        return redirect(url_for('login'))

    course = db_session.query(Course).get(course_id)
    if not course:
        flash("Course not found!", "error")
        return redirect(url_for('admin_manage_courses'))

    if request.method == 'POST':
        try:
            course.title = request.form['title']
            course.description = request.form['description']

            if 'course_thumbnail' in request.files:
                file = request.files['course_thumbnail']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join('static/img', filename))
                    course.course_thumbnail = filename

            lesson_ids = request.form.getlist('lesson_id[]')
            lesson_titles = request.form.getlist('lesson_title[]')
            lesson_contents = request.form.getlist('lesson_content[]')
            lesson_links = request.form.getlist('lesson_link[]')

            for i in range(len(lesson_titles)):
                if i < len(lesson_ids) and lesson_ids[i]:  # Ensure lesson_ids exists
                    lesson = db_session.query(Lesson).get(int(lesson_ids[i]))
                    if lesson:
                        lesson.title = lesson_titles[i]
                        lesson.content = lesson_contents[i]
                        lesson.course_link = lesson_links[i]
                else:  # If new lesson
                    new_lesson = Lesson(
                        title=lesson_titles[i],
                        content=lesson_contents[i],
                        course_link=lesson_links[i],
                        course_id=course.id
                    )
                    db_session.add(new_lesson)

            existing_quiz = db_session.query(Quiz).filter_by(course_id=course.id).first()
            if not existing_quiz:
                existing_quiz = Quiz(title=f"Quiz for {course.title}", course_id=course.id)
                db_session.add(existing_quiz)
                db_session.flush()

            quiz_ids = request.form.getlist('quiz_id[]')
            quiz_questions = request.form.getlist('quiz_question[]')
            options_A = request.form.getlist('option_A[]')
            options_B = request.form.getlist('option_B[]')
            options_C = request.form.getlist('option_C[]')
            options_D = request.form.getlist('option_D[]')
            correct_answers = request.form.getlist('correct_answer[]')

            for i in range(len(quiz_questions)):
                if i < len(quiz_ids) and quiz_ids[i]:
                    question = db_session.query(Question).get(int(quiz_ids[i]))
                    if question:
                        question.question = quiz_questions[i]
                        question.option_A = options_A[i]
                        question.option_B = options_B[i]
                        question.option_C = options_C[i]
                        question.option_D = options_D[i]
                        question.answer = correct_answers[i]
                else:
                    new_question = Question(
                        question=quiz_questions[i],
                        option_A=options_A[i],
                        option_B=options_B[i],
                        option_C=options_C[i],
                        option_D=options_D[i],
                        answer=correct_answers[i],
                        quiz_id=existing_quiz.id
                    )
                    db_session.add(new_question)

            db_session.commit()

            flash("Course and lessons updated successfully!", "success")
            return redirect(url_for('admin_manage_courses'))

        except Exception as e:
            db_session.rollback()
            flash(f"Error updating course: {e}", "error")

    return render_template('admin_update_course.html', course=course)

# View all quizzes
@app.route('/admin/manage_quizzes/')
def admin_manage_quizzes():
    if 'username' not in session or session.get('role') != 'admin':
        flash("Access Denied! Admins only.", "danger")
        return redirect(url_for('login'))

    quizzes = db_session.query(Quiz).all()
    courses = db_session.query(Course).all()  # ✅ Fetch all courses

    return render_template('admin_manage_quizzes.html', quizzes=quizzes, courses=courses)

@app.route('/admin/add_quiz/', methods=['POST'])
def admin_add_quiz():
    if 'username' not in session or session.get('role') != 'admin':
        flash("Access Denied! Admins only.", "danger")
        return redirect(url_for('login'))

    title = request.form['quiz_title']
    course_id = request.form['course_id']

    new_quiz = Quiz(title=title, course_id=course_id)
    db_session.add(new_quiz)
    db_session.commit()

    # Now, add questions
    questions = request.form.getlist('quiz_question[]')
    options_A = request.form.getlist('option_A[]')
    options_B = request.form.getlist('option_B[]')
    options_C = request.form.getlist('option_C[]')
    options_D = request.form.getlist('option_D[]')
    correct_answers = request.form.getlist('correct_answer[]')

    for q_text, opt_A, opt_B, opt_C, opt_D, correct_ans in zip(questions, options_A, options_B, options_C, options_D, correct_answers):
        new_question = Question(
            question=q_text,
            option_A=opt_A,
            option_B=opt_B,
            option_C=opt_C,
            option_D=opt_D,
            answer=correct_ans,
            quiz_id=new_quiz.id
        )
        db_session.add(new_question)

    db_session.commit()

    flash('Quiz and questions created successfully!', 'success')
    return redirect(url_for('admin_manage_quizzes'))

    # try:
    #     # Convert course_id and lesson_id to integers
    #     course_id = int(course_id)
    #     lesson_id = int(lesson_id) if lesson_id else None

    #     # Create and save the new quiz
    #     new_quiz = Quiz(title=title, course_id=course_id, lesson_id=lesson_id)
    #     db_session.add(new_quiz)
    #     db_session.commit()

    #     flash('Quiz created successfully!', 'success')
    # except ValueError:
    #     flash("Invalid Course or Lesson ID.", "danger")
    # except Exception as e:
    #     flash(f"An error occurred: {str(e)}", "danger")

    # return redirect(url_for('admin_manage_quizzes'))

# Edit a quiz
@app.route('/admin/edit_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def admin_edit_quiz(quiz_id):
    quiz = db_session.query(Quiz).options(joinedload(Quiz.quiz_questions)).filter_by(id=quiz_id).first()

    if not quiz:
        flash('Quiz not found!', 'danger')
        return redirect(url_for('admin_manage_quizzes'))
    
    if request.method == 'POST':
        # Update quiz title
        quiz.title = request.form['title']

        # --- Update Existing Questions ---
        for question in quiz.quiz_questions:
            question.question = request.form.get(f'question_{question.id}')
            question.option_A = request.form.get(f'option_A_{question.id}')
            question.option_B = request.form.get(f'option_B_{question.id}')
            question.option_C = request.form.get(f'option_C_{question.id}')
            question.option_D = request.form.get(f'option_D_{question.id}')
            question.answer = request.form.get(f'answer_{question.id}')

        # --- Add New Questions ---
        new_questions = request.form.getlist('new_question[]')
        new_options_A = request.form.getlist('new_option_A[]')
        new_options_B = request.form.getlist('new_option_B[]')
        new_options_C = request.form.getlist('new_option_C[]')
        new_options_D = request.form.getlist('new_option_D[]')
        new_answers = request.form.getlist('new_answer[]')

        for q_text, opt_A, opt_B, opt_C, opt_D, ans in zip(new_questions, new_options_A, new_options_B, new_options_C, new_options_D, new_answers):
            if q_text and ans: 
                new_question = Question(
                    question=q_text,
                    option_A=opt_A,
                    option_B=opt_B,
                    option_C=opt_C,
                    option_D=opt_D,
                    answer=ans,
                    quiz_id=quiz.id 
                )
                db_session.add(new_question)

        db_session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('admin_manage_quizzes'))

    return render_template('admin_edit_quiz.html', quiz=quiz)

# Delete a quiz
@app.route('/admin/delete_quiz/<int:quiz_id>', methods=['POST', 'GET'])
def admin_delete_quiz(quiz_id):
    quiz = db_session.query(Quiz).filter_by(id=quiz_id).first()
    if quiz:
        db_session.delete(quiz)
        db_session.commit()
        flash('Quiz deleted successfully.', 'success')
    else:
        flash('Quiz not found.', 'danger')
    return redirect(url_for('admin_manage_quizzes'))

@app.route('/admin/delete_question/<int:question_id>', methods=['GET'])
def delete_question(question_id):
    question = db_session.query(Question).filter_by(id=question_id).first()
    if question:
        db_session.delete(question)
        db_session.commit()
        flash('Question deleted successfully.', 'success')
    else:
        flash('Question not found.', 'danger')
    return redirect(request.referrer)


@app.route('/admin_dashboard/')
def admin_dashboard():
    if 'username' not in session or session.get('role') != 'admin':
        flash("Access Denied! Admins only.", "danger")
        return redirect(url_for('login')) 
    
    # username = session['username']
    # user = user_db.get(username)
    # password = user['password']

    # print(f"Admin: {username}, Password: {password}")

    user = db_session.query(Users).filter_by(username=session['username']).first()
    courses = db_session.query(Course).all()

    return render_template('admin_dashboard.html',user = user, courses=courses ) 
        

@app.route('/user_dashboard/')
def user_dashboard():
    if 'username' not in session or session.get('role') != 'user':
        flash("Access Denied! Users only.", "danger")
        return redirect(url_for('login')) 

    user = db_session.query(Users).filter_by(username=session['username']).first()

    # Fetch only courses the user is enrolled in
    enrolled_courses = (
        db_session.query(Course)
        .join(Enrollment, Enrollment.course_id == Course.id)
        .filter(Enrollment.user_id == user.id)
        .all()
    )

    return render_template('user_dashboard.html', user=user, courses=enrolled_courses)

@app.route('/user_progress/')
def user_progress():
    user = db_session.query(Users).filter_by(username=session['username']).first()
    enrolled_courses = db_session.query(Enrollment).filter_by(user_id=user.id).all()
    quiz_results = db_session.query(QuizResult).filter_by(user_id=user.id).all()

    return render_template('user_progress.html', user=user, enrolled_courses=enrolled_courses, quiz_results=quiz_results)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


courses_added = False

@app.before_request
def initialize_courses():
    global courses_added
    if not courses_added:
        # add_courses()
        courses_added = True

@app.route('/logout/')
def logout():
    session.pop('username', None) 
    session.pop('role', None) 
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
