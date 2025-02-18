from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
from werkzeug.utils import secure_filename #type: ignore
from io import BytesIO
from werkzeug.security import generate_password_hash, check_password_hash   # type: ignore
from database import session as db_session
from models import Course, Users, Lesson,Question,QuizResult, Contact, Enrollment
import json

app = Flask(__name__,
            template_folder='templates', 
            static_folder='static')
app.config['SECRET_KEY'] = '9224ab35a0fb246961b5d55a' 


user_db = {}

admin_username = 'Shahid'
admin_password = 'Flask@123'

user_db[admin_username] = {
    'fname': 'Shahid',
    'lname': 'Raja',
    'email': 'admin@gmail.com',
    'password': generate_password_hash(admin_password),
    'role' : 'admin'
}

default_user_username = 'user1'
default_password = 'User1@123'

if default_user_username not in user_db:
    user_db[default_user_username] = {
        'fname': 'User',
        'lname': '1',
        'email': 'user1@gmail.com',
        'password': generate_password_hash(default_password),
        'course': [],
        'role' : 'user'
    }
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

        # user = db_session.query(Users).filter_by(username=username).first()
        user = user_db.get(username)

        if user and check_password_hash(user['password'], password):
            # login_user(user)
            session['username'] = username
            session['role'] = user['role']

            flash("Login successful!", "success")

            if user['role'] == 'admin':
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
        
        # existing_user = db_session.query(Users).filter_by(username=username).first()

        if username in user_db:
            flash("Username already exists", "error")
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)

        role = 'user'

        user_db[username] = {
            'fname': fname,
            'lname': lname,
            'email': email,
            'password': hashed_password,
            'role': role
        }
        # if Users.query.filter_by(username=username).first():
        #     flash("Username already exists", "error")
        #     return render_template('register.html',email=email)
        # if Users.query.filter_by(email=email).first():
        #     flash("Email already exists","error")
        #     return render_template('register.html',username=username)
        
        # role = request.form.get('role', 'user')

        # hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = Users(fname=fname, lname=lname,username=username, email=email, password=password_confirmation, role=role)

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
    try:
        course = db_session.query(Course).get(course_id)
        if request.method == 'POST':
            user_id = request.form.get('user_id')  
            user = Users.query.get_or_404(user_id)

            existing_enrollment = Enrollment.query.filter_by(user_id=user.id, course_id=course.id).first()

            if existing_enrollment:
                flash('You are already enrolled in this course.', 'info')
            else:
                enrollment = Enrollment(user_id=user.id, course_id=course.id)
                db_session.add(enrollment)
                db_session.commit() 
                flash(f'You have successfully enrolled in {course.title}!', 'success')

            return redirect(url_for('course_list')) 
        return render_template('courses.html', course=course)
    
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
        return redirect(url_for('course_content')) 
    

@app.route('/user_courses/')
def user_courses():
    user = db_session.query(Users).get(1)
    if user:
        courses = user.course  # Access the courses the user is enrolled in
        return render_template('user_courses.html', user=user, courses=courses)
    return "User not found", 404



@app.route('/certificate/')
def certificate():
    return render_template('certificate.html')

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
    
    users = db_session.query(Users).all()
    return render_template('admin_manage_users.html', users=users)

# Route to add a new user
@app.route('/admin/add_user/', methods=['GET', 'POST'])
def admin_add_user():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

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
        flash("User added successfully!", "success")
        return redirect(url_for('admin_manage_users'))
    
    return render_template('admin_add_user.html')

# Route to edit user details
@app.route('/admin/edit_user/<int:user_id>/', methods=['GET', 'POST'])
def admin_edit_user(user_id):
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    user = db_session.query(Users).get(user_id)

    if not user:
        flash("User not found!", "error")
        return redirect(url_for('admin_manage_users'))
    
    if request.method == 'POST':
        user.fname = request.form.get('fname')
        user.lname = request.form.get('lname')
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        # user.password = generate_password_hash(request.form['password'])
        if 'password' in request.form and request.form['password']:
            user.password = generate_password_hash(request.form['password'])

        user.role = request.form.get('role')
        db_session.commit()
        flash("User updated successfully!", "success")
        return redirect(url_for('admin_manage_users'))
    
    return render_template('admin_edit_user.html', user=user)

# Route to delete a user
@app.route('/admin/delete_user/<int:user_id>/', methods=['POST'])
def admin_delete_user(user_id):
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    user_to_delete = db_session.query(Users).get(user_id)

    if not user_to_delete:
        flash("User not found!", "error")
        return redirect(url_for('admin_manage_users'))
    
    if request.method == 'POST':
        db_session.delete(user_to_delete)
        db_session.commit()
        flash("User deleted successfully!", "success")
    else:
        flash("User not found!", "error")

    return redirect(url_for('admin_manage_users'))

# Route to confirm user deletion
@app.route('/admin/delete_user/<int:user_id>/', methods=['GET'])
def admin_delete_user_page(user_id):
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    # Fetch user data to confirm deletion
    user = db_session.query(Users).get(user_id)
    
    if not user:
        flash("User not found!", "error")
        return redirect(url_for('admin_manage_users'))
    
    return render_template('admin_delete_user.html', user=user)


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
    course = None
    if request.method == 'POST':
        try:
            title = request.form['title']  # Get from form
            description = request.form['description']  # Get from form
            course_thumbnail = None
            #request.form.get('course_thumbnail') # Optional thumbnail

            if 'course_thumbnail' in request.files:
                file = request.files['course_thumbnail']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join('static/img', filename))
                    course_thumbnail = filename

            lessons_data_str = request.form.get('lessons')
            if lessons_data_str: # Check if it's not None or empty
                try:
                    lessons_list = json.loads(lessons_data_str)  # Parse JSON
                except json.JSONDecodeError as e:
                    db_session.rollback() # Important to rollback on error
                    flash(f"Invalid JSON for lessons: {e}", "error")
                    return render_template('admin_add_course.html') # Return to the form
            else:
                lessons_list = [] # Handle the case where no lessons are provided

            new_course = Course(title=title, description=description, course_thumbnail=course_thumbnail)
            db_session.add(new_course)
            db_session.flush() # Get the new course ID

            for lesson in lessons_list:
                new_lesson = Lesson(
                    title=lesson['title'],
                    content=lesson['content'],
                    course_link=lesson['course_link'],
                    course_id=new_course.id
                )
                db_session.add(new_lesson)

            db_session.commit()
            flash("Course and lessons added successfully.", "success")
            return redirect(url_for('admin_manage_courses')) # Redirect after success

        except Exception as e:
            db_session.rollback() # Rollback on error
            flash(f"Error adding course: {e}", "error")
            print(f"Error details: {e}") #Print for debugging
            return render_template('admin_add_course.html') # Return to form on error

    return render_template('admin_add_course.html', course=course)

@app.route('/course/<int:course_id>/')
def course_content(course_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    course = db_session.query(Course).get(course_id)
    if not course:
        flash("Course not found!", "error")
        return redirect(url_for('course_list'))
    
    user = db_session.query(Users).filter_by(username=session['username']).first()
    if not user or not user.is_enrolled(course):
        flash("You need to enroll in this course to access lessons.", "warning")
        # return redirect(url_for('course_list'))

    return render_template('course_content.html', course=course)

@app.route('/course/<int:course_id>/lesson/<int:lesson_id>/')
def start_lesson(course_id, lesson_id):
    course = db_session.query(Course).get(course_id)
    lesson = db_session.query(Lesson).get(lesson_id)
    if not lesson:
        flash("Lesson not found!", "error")
        return redirect(url_for('course_content', course_id=course_id))
    return render_template('start_lesson.html', lesson=lesson,course_id=course_id)


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
        return redirect(url_for('login'))
    
    course = db_session.query(Course).get(course_id)
    if not course:
        flash("Course not found!", "error")
        return redirect(url_for('admin_manage_courses'))
    
    if request.method == 'POST':

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
            if lesson_ids and lesson_ids[i]:  # Existing lesson
                lesson = db_session.query(Lesson).get(lesson_ids[i])
                if lesson:
                    lesson.title = lesson_titles[i]
                    lesson.content = lesson_contents[i]
                    lesson.course_link = lesson_links[i]
            else:  # New lesson
                new_lesson = Lesson(
                    title=lesson_titles[i],
                    content=lesson_contents[i],
                    course_link=lesson_links[i],
                    course_id=course.id
                )
                db_session.add(new_lesson)

        db_session.commit()

        flash("Course and lessons updated successfully!", "success")
        return redirect(url_for('admin_manage_courses'))
    
    return render_template('admin_update_course.html', course=course)

@app.route('/admin/reports/')
def admin_reports():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    # Render reports page
    return render_template('admin_reports.html')

@app.route('/admin_dashboard/')
def admin_dashboard():
    if 'username' not in session or session.get('role') != 'admin':
        flash("Access Denied! Admins only.", "danger")
        return redirect(url_for('login')) 
    
    # username = session['username']
    # user = user_db.get(username)
    # password = user['password']

    # print(f"Admin: {username}, Password: {password}")

    return render_template('admin_dashboard.html', 
        user={'username': session['username'], 'email': user_db[session['username']]['email']})

@app.route('/user_dashboard/')
def user_dashboard():
    if 'username' not in session or session.get('role') != 'user':
        flash("Access Denied! Users only.", "danger")
        return redirect(url_for('login')) 
    
    username = session['username']  # The username from the session

    return render_template('user_dashboard.html', 
        user={'username': username, 'email': user_db[username]['email']})

@app.route('/user_progress/')
def user_progress():
    return render_template('user_progress.html')
 
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
