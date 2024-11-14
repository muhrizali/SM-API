from flask import Flask, request
from flask_restful import Resource, Api, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy import select, delete, and_
from sqlalchemy.orm import DeclarativeBase, Session

# initializing flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'
db = SQLAlchemy(app)
api = Api(app)

# initilizing database orm
engine = db.create_engine("sqlite:///api_database.sqlite3")


class Base(DeclarativeBase):
    pass


# initilizing tables
class Student(Base):
    __tablename__ = "student"
    student_id = Column(Integer, primary_key=True, autoincrement="auto")
    roll_number = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String)


class Course(Base):
    __tablename__ = "course"
    course_id = Column(Integer, primary_key=True, autoincrement="auto")
    course_code = Column(String, unique=True, nullable=False)
    course_name = Column(String, nullable=False)
    course_description = Column(String)


class Enrollment(Base):
    __tablename__ = "enrollments"
    enrollment_id = Column(Integer, primary_key=True, autoincrement="auto")
    estudent_id = Column(Integer, ForeignKey("student.student_id"), nullable=False)
    ecourse_id = Column(Integer, ForeignKey("course.course_id"), nullable=False)


# creating tables
Base.metadata.create_all(engine)


# helpful table db functions
# All helpful functions for Course resources
def get_first_course(id):
    with Session(engine) as session:
        db_response = session.get(Course, id)
        return db_response


def get_all_courses(id):
    with Session(engine) as session:
        if id is not None:
            select_objs = select(Course).where(Course.course_id == id)
        else:
            select_objs = select(Course)
        db_response = session.scalars(select_objs).all()
        return db_response


def course_exists(id):
    with Session(engine) as session:
        select_objs = select(Course).where(Course.course_id == id)
        db_response = session.scalars(select_objs).all()
        db_response_list = list(db_response)
        if len(db_response_list):
            return True
        else:
            return False


def course_code_exists(new_course_code):
    with Session(engine) as session:
        select_objs = select(Course).where(Course.course_code == new_course_code)
        db_response = session.scalars(select_objs).all()
        db_response_list = list(db_response)
        if len(db_response_list):
            return True
        else:
            return False


def update_course(id, update_data):
    with Session(engine) as session:
        course_obj = session.get(Course, id)
        course_obj.course_name = update_data["course_name"]
        course_obj.course_code = update_data["course_code"]
        course_obj.course_description = update_data["course_description"]
        session.commit()


def delete_course(id):
    with Session(engine) as session:
        course_obj = session.get(Course, id)
        session.delete(course_obj)
        session.commit()


def create_course(create_data):
    with Session(engine) as session:
        course_obj = Course(
            course_code=create_data["course_code"],
            course_name=create_data["course_name"],
            course_description=create_data["course_description"]
        )
        session.add(course_obj)
        session.commit()

    with Session(engine) as session:
        select_obj = select(Course).where(Course.course_code == create_data["course_code"])
        created_obj = session.scalars(select_obj).first()
        return created_obj


# All helpful functions for Student resources
def get_first_student(id):
    with Session(engine) as session:
        db_response = session.get(Student, id)
        return db_response


def get_all_students(id):
    with Session(engine) as session:
        if id is not None:
            select_objs = select(Student).where(Student.student_id == id)
        else:
            select_objs = select(Student)
        db_response = session.scalars(select_objs).all()
        return db_response


def student_exists(id):
    with Session(engine) as session:
        select_objs = select(Student).where(Student.student_id == id)
        db_response = session.scalars(select_objs).all()
        db_response_list = list(db_response)
        if len(db_response_list):
            return True
        else:
            return False


def student_roll_exists(new_roll_num):
    with Session(engine) as session:
        select_objs = select(Student).where(Student.roll_number == new_roll_num)
        db_response = session.scalars(select_objs).all()
        db_response_list = list(db_response)
        if len(db_response_list):
            return True
        else:
            return False


def update_student(id, update_data):
    with Session(engine) as session:
        student_obj = session.get(Student, id)
        student_obj.roll_number = update_data["roll_number"]
        student_obj.first_name = update_data["first_name"]
        student_obj.last_name = update_data["last_name"]
        session.commit()


def delete_student(id):
    with Session(engine) as session:
        student_obj = session.get(Student, id)
        session.delete(student_obj)
        session.commit()


def create_student(create_data):
    with Session(engine) as session:
        student_obj = Student(
            roll_number=create_data["roll_number"],
            first_name=create_data["first_name"],
            last_name=create_data["last_name"]
        )
        session.add(student_obj)
        session.commit()

    with Session(engine) as session:
        select_obj = select(Student).where(Student.roll_number == create_data["roll_number"])
        created_obj = session.scalars(select_obj).first()
        return created_obj


# All helpful functions for Enrollment resources
def get_all_enrollments(id):
    with Session(engine) as session:
        select_objs = select(Enrollment).where(Enrollment.estudent_id == id)
        db_response = session.scalars(select_objs).all()
        return db_response


def enroll_student_to_course(student_id, course_id):
    with Session(engine) as session:
        enroll_obj = Enrollment(
            estudent_id=student_id,
            ecourse_id=course_id
        )
        session.add(enroll_obj)
        session.commit()


def delete_enrollment(student_id, course_id):
    with Session(engine) as session:
        delete_objs = delete(Enrollment).where(
            and_(
                Enrollment.estudent_id == student_id,
                Enrollment.ecourse_id == course_id
            )
        )
        session.execute(delete_objs)
        session.commit()


# testing api
class TestingAPI(Resource):
    def get(self):
        return {
            "hello": "world!"
        }


# Building APIs

# Setting Up APIs for Courses
class CourseAPI(Resource):
    def get(self, course_id):
        course_in_db = course_exists(course_id)
        if course_in_db:

            db_object = get_first_course(id=course_id)
            return {
                "course_id": db_object.course_id,
                "course_name": db_object.course_name,
                "course_code": db_object.course_code,
                "course_description": db_object.course_description
            }, 200
        else:
            return abort(404, message="Course Not Found")

    def put(self, course_id):
        update_data = request.form

        if "course_code" not in update_data.keys():
            return abort(400, error_code="COURSE002", error_message="Course Code is required")

        if "course_name" not in update_data.keys():
            return abort(400, error_code="COURSE001", error_message="Course Name is required")

        course_in_db = course_exists(course_id)
        if not course_in_db:
            return abort(404, message="Course Not Found")
        else:
            update_course(id=course_id, update_data=update_data)
            db_object = get_first_course(id=course_id)
            return {
                "course_id": db_object.course_id,
                "course_name": db_object.course_name,
                "course_code": db_object.course_code,
                "course_description": db_object.course_description
            }, 200

    def delete(self, course_id):
        course_in_db = course_exists(course_id)
        if not course_in_db:
            return abort(404, message="Course Not Found")
        else:
            delete_course(id=course_id)


class CourseCreateAPI(Resource):
    def post(self):

        course_data = request.form

        if "course_code" not in course_data.keys():
            return abort(400, error_code="COURSE002", error_message="Course Code is required")

        if "course_name" not in course_data.keys():
            return abort(400, error_code="COURSE001", error_message="Course Name is required")

        new_course_code = course_data["course_code"]
        course_in_db = course_code_exists(new_course_code=new_course_code)
        if course_in_db:
            return abort(409, message="Course already exists")
        else:
            db_response = create_course(course_data)
            return {
                "course_id": db_response.course_id,
                "course_code": db_response.course_code,
                "course_name": db_response.course_name,
                "course_description": db_response.course_description
            }, 201


# Setting up APIs for Students
class StudentAPI(Resource):
    def get(self, student_id):
        student_in_db = student_exists(student_id)
        if student_in_db:
            db_object = get_first_student(id=student_id)
            return {
                "student_id": db_object.student_id,
                "roll_number": db_object.roll_number,
                "first_name": db_object.first_name,
                "last_name": db_object.last_name
            }, 200
        else:
            return abort(404, message="Student Not Found")

    def put(self, student_id):
        update_data = request.form

        if "roll_number" not in update_data.keys():
            return abort(400, error_code="STUDENT001", error_message="Roll Number is required")

        if "first_name" not in update_data.keys():
            return abort(400, error_code="STUDENT002", error_message="First Name is required")

        student_in_db = student_exists(student_id)
        if not student_in_db:
            return abort(404, message="Student Not Found")
        else:
            update_student(id=student_id, update_data=update_data)
            db_object = get_first_student(id=student_id)
            return {
                "student_id": db_object.student_id,
                "roll_number": db_object.roll_number,
                "first_name": db_object.first_name,
                "last_name": db_object.last_name
            }, 200

    def delete(self, student_id):
        student_in_db = student_exists(student_id)
        if not student_in_db:
            return abort(404, message="Student Not Found")
        else:
            delete_student(id=student_id)


class StudentCreateAPI(Resource):
    def post(self):
        student_data = request.form

        if "roll_number" not in student_data.keys():
            return abort(400, error_code="STUDENT001", error_message="Roll Number is required")

        if "first_name" not in student_data.keys():
            return abort(400, error_code="STUDENT002", error_message="First Name is required")

        new_roll_num = student_data["roll_number"]
        student_in_db = student_roll_exists(new_roll_num=new_roll_num)
        if student_in_db:
            return abort(409, message="Student already exists")
        else:
            db_response = create_student(student_data)
            return {
                "student_id": db_response.student_id,
                "roll_number": db_response.roll_number,
                "first_name": db_response.first_name,
                "last_name": db_response.last_name
            }, 201


# Setting up APIs for Enrollment resources
class EnrollmentAPI(Resource):
    def get(self, student_id):
        student_in_db = student_exists(id=student_id)
        if not student_in_db:
            return abort(400, error_code="ENROLLMENT002", error_message="Student does not exist")

        enrollment_list = []
        enrollments = get_all_enrollments(id=student_id)
        for enrollment in enrollments:
            enroll_obj = {
                "enrollment_id": enrollment.enrollment_id,
                "student_id": enrollment.estudent_id,
                "course_id": enrollment.ecourse_id
            }
            enrollment_list.append(enroll_obj)

        if not len(enrollment_list):
            return abort(404, message="Student is not enrolled in any course")
        else:
            return enrollment_list

    def post(self, student_id):
        enroll_data = request.form
        course_id = enroll_data["course_id"]

        student_in_db = student_exists(id=student_id)
        course_in_db = course_exists(id=course_id)

        if not course_in_db:
            return abort(400, error_code="ENROLLMENT001", error_message="Course does not exist")
        if not student_in_db:
            return abort(404, message="Student not found")
        else:
            enroll_student_to_course(student_id=student_id, course_id=course_id)
            enrollment_list = []
            enrollments = get_all_enrollments(id=student_id)
            for enrollment in enrollments:
                enroll_obj = {
                    "enrollment_id": enrollment.enrollment_id,
                    "student_id": enrollment.estudent_id,
                    "course_id": enrollment.ecourse_id
                }
                enrollment_list.append(enroll_obj)
            return enrollment_list, 201


class EnrollmentDeleteAPI(Resource):

    def delete(self, student_id, course_id):
        student_in_db = student_exists(id=student_id)
        course_in_db = course_exists(id=course_id)

        if not course_in_db:
            return abort(400, error_code="ENROLLMENT001", error_message="Course does not exist")
        if not student_in_db:
            return abort(400, error_code="ENROLLMENT002", error_message="Student does not exist")

        enrollments = get_all_enrollments(id=student_id)
        if not len(list(enrollments)):
            return abort(404, message="Enrollment for the student not found")

        else:
            delete_enrollment(student_id=student_id, course_id=course_id)


# Mapping Testing API
api.add_resource(TestingAPI, "/api/")

# Mapping course APIs
api.add_resource(CourseAPI, "/api/course/<int:course_id>")
api.add_resource(CourseCreateAPI, "/api/course")

# Mapping student APIs
api.add_resource(StudentAPI, "/api/student/<int:student_id>")
api.add_resource(StudentCreateAPI, "/api/student")

# Mapping enrollment APIs
api.add_resource(EnrollmentAPI, "/api/student/<int:student_id>/course")
api.add_resource(EnrollmentDeleteAPI, "/api/student/<int:student_id>/course/<int:course_id>")

if __name__ == '__main__':
    app.run(debug=True)
