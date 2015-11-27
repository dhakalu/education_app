import hmac
import re
from google.appengine.ext import endpoints
from protorpc import remote
from protorpc import message_types
from protorpc import messages
import tables
import utility

NAME_RE = re.compile("^[a-zA-Z]{3,100}$")
EMAIL_RE = re.compile("^[\S]+@[\S]+\.[\S]+$")
PASS_RE = re.compile("^.{5,20}$")


class Student(messages.Message):
    first_name = messages.StringField(1, required=True)
    last_name = messages.StringField(2, required=True)
    user_name = messages.StringField(3, required=True)
    email = messages.StringField(4, required=True)
    password = messages.StringField(5, required=True)
    school = messages.StringField(6, required=True)


@endpoints.api(name='userapi', version='v1',
               description="user api")
class UserApi(remote.Service):
    @endpoints.method(Student, Student,
                      name='sign_up',
                      path="signup",
                      http_method='POST')
    def sign_up(self, request):
        """
        This is the method that adds the user to the database, provided the  information
        submitted by clients are valid
        :param request: student object requested by the user to add to the database
        :return: The user object that has been registered
        """
        first_name = request.first_name
        last_name = request.last_name
        user_name = request.user_name
        is_valid_name(user_name)
        email = request.email
        password = request.password
        school = request.school
        is_valid_email(email)
        if not is_valid_password(password):
            raise endpoints.BadRequestException("Passowrd is not valid")

        tables.StudentModel(first_name=first_name, last_name=last_name,
                            user_name=user_name, email=email,
                            is_verified=False, school=school,
                            password=utility.hash_str(password)).put()
        schools = school.split(",");

        return Student(first_name=first_name,
                       last_name=last_name,
                       user_name=user_name,
                       email='',
                       password='',
                       school=school)


###################################################
#
# UTILITY FUNCTIONS
#
###################################################

def is_valid_name(username):
    """
    Checks if the given username is valid
    :param username: The username provided by the client
    :return: True if the name is valid false otherwise
    """
    if username and NAME_RE.match(username):
        if tables.StudentModel.by_name(username):
            raise endpoints.BadRequestException('Username exists.'
                                                'Choose another.')
    else:
        endpoints.BadRequestException('Username is not valid.')


def is_valid_password(password):
    """
        this is the method that ckecks if the password is valid
    """
    return password and PASS_RE.match(password)


def is_valid_email(email):
    """
    Checks if the email requested by user is a valid email
    :param email Email passed by the user
    :raises BadRequestException when the email already exists in the db
        or the email is not valid
    """
    if email and EMAIL_RE.match(email):
        if tables.StudentModel.by_email(email):
            raise endpoints.BadRequestException('There is an account '
                                                'associated with that email.')
    else:
        raise endpoints.BadRequestException('Email is not valid')


