from google.appengine.ext import db


class StudentModel(db.Model):
    """ This is the class that defines the student object
    @author: Upendra Dhakal
    """
    # Basic information
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    user_name = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)

    # password used to login
    password = db.StringProperty(required=True)

    # check if the user is verified
    is_verified = db.BooleanProperty(required=True)

    # date on which the user signed up
    signup_date = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_name(cls, username):
        return StudentModel.all().filter("user_name =", username).get()

    @classmethod
    def by_email(cls, email):
        return StudentModel.all().filter("email =", email).get()


class SchoolModel(db.Model):
    """This is the class that describes the schema of the school model
    To create this object following args must be passed
    @:arg name string that represents the name of the school
    """
    name = db.StringProperty(required=True)
    address = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    url = db.LinkProperty(required=True)
    created_on = db.DateTimeProperty(auto_now_add=True)


class CourseModel(db.Model):
    course_id = db.StringProperty()
    title = db.StringProperty()
    school = db.ReferenceProperty(SchoolModel, collection_name="courses")


class CourseStudent(db.Model):
    """
    One student can take more than one courses at the same time and the course can hold
    more than one student. Hence student and courses have many to many relation
    This table creates the relation between course model and student model
    """
    course = db.ReferenceProperty(StudentModel, required=True,
                                  collection_name='courses')
    student = db.ReferenceProperty(CourseModel, required=True,
                                   collection_name='students')


class SchoolStudent(db.Model):
    """
    One student might be associated with both MIT and Harvard by cross registration or
    something
    """
    student = db.ReferenceProperty(CourseModel, required=True,
                                   collection_name='students')

    school = db.ReferenceProperty(SchoolModel, required=True,
                                  collection_name='schools')


class PostModel(db.Model):
    post = db.TextProperty(required=True)
    user_name = db.StringProperty(required=True)
    posted_on = db.DateTimeProperty(auto_now_add=True)


class CommentModel(db.Model):
    post = db.ReferenceProperty(PostModel, "comments")
    comment = db.TextProperty(required=True)
    user_name = db.StringProperty(required=True)
    commented_on = db.DateTimeProperty(auto_now_add=True)

