from google.appengine.ext import endpoints
from protorpc import message_types
from protorpc import messages
from protorpc import remote
import tables
import user_api


class School(messages.Message):
    """ Thi is the class used to pass the list of schools
        when the request is made in the url get all schools
    """
    name = messages.StringField(1, required=True)


class Course(messages.Message):
    # course id is the abbreviated name of the course CS101 for example
    course_id = messages.StringField(1, required=True)
    # title is the full name of the course like Introduction to CS
    title = messages.StringField(2, required=True)
    # to which the course belongs to
    # unique_id given to the college
    school = messages.StringField(3, required=True)


class CollegeList(messages.Message):
    """
    this is the class that creates the list of the colleges to
    send as the message
    """
    items = messages.MessageField(School, 1, repeated=True)


class CourseList(messages.Message):
    """
    This is the class that is creates the list of courses to
    send as the message
    """
    items = messages.MessageField(Course, 1, repeated=True)


@endpoints.api(name='classes', version='v1',
               description="Api for the courses")
class ClassApi(remote.Service):
    """
    This is the api
    """

    @endpoints.method(Course, Course,
                      name='add_course',
                      path='add_course',
                      http_method='POST')
    def add_course(self, request):
        """
        This is the method that provides the api to add the course to the
        database
        :param request: This is the request object that contains query information
        :return: Returns the course that has been added to the db
        """
        sch = tables.SchoolModel.get_by_id(int(request.school))
        if sch:
            tables.CourseModel(school=sch, course_id=request.course_id,
                               title=request.title).put()
            return Course(course_id=request.course_id, title=request.title, school=request.school)
        else:
            raise endpoints.BadRequestException("Invalid college Id")

    @endpoints.method(message_types.VoidMessage, CollegeList,
                      name='get_all_schools',
                      path='get_schools',
                      http_method='GET')
    def get_schools(self, unused_request):
        """
        This is the method that returns the list of the schools to
         the client who requested for the information
        :param unused_request: The request object send by the client
        :return: The list of the colleges/schools
        """
        colleges = []
        for college in tables.SchoolModel.all():
            colleges.append(School(name=college.name))
        return CollegeList(items=colleges)

    @endpoints.method(School, CourseList,
                      name='get_all_courses_by_college',
                      path='/get_courses',
                      http_method='GET')
    def get_courses(self, request):
        """
        This is the method that returns the list of the courses
        :param request: The request object that contains the information about the
        school
        :return: List of the courses offered by the given school
        """
        courses = []
        for course in tables.SchoolModel.get_by_id(int(request.name)).courses:
            print course.school.key
            courses.append(Course(course_id=course.course_id,
                                  school=course.school.name,
                                  title=course.title))
        return CourseList(items=courses)

    def enroll(self, request):
        """
        This is the method that adds the offered courses to the user's course list
        :param request: The object that contains the information about the user
        :return: The course that has been added to the course list
        """
        pass


application = endpoints.api_server([ClassApi, user_api.UserApi])
