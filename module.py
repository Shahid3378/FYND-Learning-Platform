# course.py
class Course:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.lessons = []

    def add_lesson(self, lesson):
        self.lessons.append(lesson)

    def __repr__(self):
        return f"Course(name={self.name}, description={self.description}, lessons={len(self.lessons)})"


class CourseManager:
    def __init__(self):
        self.courses = []

    def create_course(self, name, description):
        course = Course(name, description)
        self.courses.append(course)
        print(f"Course '{name}' created successfully!")

    def list_courses(self):
        if not self.courses:
            print("No courses available.")
        for idx, course in enumerate(self.courses, 1):
            print(f"{idx}. {course.name} - {course.description} (Lessons: {len(course.lessons)})")

    def find_course_by_name(self, name):
        for course in self.courses:
            if course.name.lower() == name.lower():
                return course
        return None


def main():
    course_manager = CourseManager()

    while True:
        print("\n--- Course Management ---")
        print("1. Create Course")
        print("2. List Courses")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter course name: ")
            description = input("Enter course description: ")
            course_manager.create_course(name, description)
        elif choice == "2":
            course_manager.list_courses()
        elif choice == "3":
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()

# lesson.py
class Lesson:
    def __init__(self, name, description, course):
        self.name = name
        self.description = description
        self.course = course  # Link this lesson to a course

    def __repr__(self):
        return f"Lesson(name={self.name}, description={self.description}, course={self.course.name})"


class LessonManager:
    def __init__(self):
        self.lessons = []

    def create_lesson(self, name, description, course):
        lesson = Lesson(name, description, course)
        self.lessons.append(lesson)
        course.add_lesson(lesson)
        print(f"Lesson '{name}' created successfully and added to the course '{course.name}'!")

    def list_lessons(self):
        if not self.lessons:
            print("No lessons available.")
        for lesson in self.lessons:
            print(f"{lesson.name} - {lesson.description} (Course: {lesson.course.name})")


def main():
    course_manager = CourseManager()
    lesson_manager = LessonManager()

    # Sample interaction with the course manager
    while True:
        print("\n--- Lesson Management ---")
        print("1. Create Lesson")
        print("2. List Lessons")
        print("3. List Courses")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            if not course_manager.courses:
                print("No courses available. Please create a course first.")
                continue
            course_manager.list_courses()
            course_name = input("Enter the course name to add lesson: ").strip()
            course = course_manager.find_course_by_name(course_name)

            if not course:
                print("Course not found!")
                continue

            lesson_name = input("Enter lesson name: ")
            lesson_description = input("Enter lesson description: ")
            lesson_manager.create_lesson(lesson_name, lesson_description, course)
        elif choice == "2":
            lesson_manager.list_lessons()
        elif choice == "3":
            course_manager.list_courses()
        elif choice == "4":
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()

