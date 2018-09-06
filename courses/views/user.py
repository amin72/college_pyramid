from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid.security import unauthenticated_userid

from ..services.user import UserService
from ..models.user import User
from ..models.courses import Student



@view_config(route_name='home',
             renderer='courses:templates/index.jinja2')
def index_page(request):
    return {}



@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    username = request.POST.get('username')
    if username:
        user = UserService.by_name(username, request=request)
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.id)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)



@view_config(route_name='student_information',
    renderer='courses:templates/student_information.jinja2')
def student_information(request):
    if not request.user:
        return HTTPFound(location=request.route_url('home'))

    student = request.dbsession.query(Student).filter_by(
        user=request.user).first()
    return {'student': student}



@view_config(route_name='edit_student_information',
    renderer='courses:templates/edit_student_information.jinja2')
def edit_student_information(request):
    if not request.user:
        return HTTPFound(location=request.route_url('home'))

    student = request.dbsession.query(Student).filter_by(
        user=request.user).first()
    return {'student': student}



@view_config(route_name='update_student_information',
    request_method='POST', renderer='string')
def update_student_information(request):
    if not request.user:
        return HTTPFound(location=request.route_url('home'))

    user = request.user

    user.firstname = request.params.get('firstname')
    user.lastname = request.params.get('lastname')
    user.phone = request.params.get('phone')
    user.address = request.params.get('address')

    return HTTPFound(request.route_url('student_information'))



def get_user(request):
    user = request.dbsession.query(User).filter_by(
        id=request.authenticated_userid).first()
    return user
