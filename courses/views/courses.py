from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget

from ..models.user import User
from ..models.courses import Course, Student, Teacher, Major, SelectedCourses



MAX_CREDITS = 20



@view_config(route_name='courses',
             renderer='courses:templates/courses.jinja2')
def courses_view(request):
	student = request.dbsession.query(Student).filter_by(user=request.user).first()

	selected_courses = request.dbsession.query(SelectedCourses
		).filter_by(student=student).all()

	credits = 0
	for s in selected_courses:
		credits += s.course.credits

	return {'selected_courses': selected_courses, 'credits': credits}



@view_config(route_name='select_courses',
             renderer='courses:templates/select_courses.jinja2')
def selected_courses_view(request):
	user = request.user
	student = request.dbsession.query(Student).filter_by(user=user).first()
	
	selected_courses = request.dbsession.query(SelectedCourses
		).filter_by(student=student).all()
	
	available_courses = request.dbsession.query(Course
		).filter_by(major=student.major)

	available_courses_for_student = []
	for c in available_courses:
		available = True
		for s in selected_courses:
			if s.course.id == c.id:
				available = False
				break
		
		if available:
			available_courses_for_student.append(c)
	

	credits = 0
	for s in selected_courses:
		credits += s.course.credits

	return {'selected_courses': selected_courses,
			'available_courses': available_courses_for_student,
			'credits': credits,
	}



@view_config(route_name='add_course',
             renderer='string')
def add_course(request):
	user = request.user
	student = request.dbsession.query(Student).filter_by(user=user).first()

	course_id = int(request.matchdict.get('id', -1))
	course = request.dbsession.query(Course).filter_by(id=course_id).first()

	if course.signed_up_students >= course.allowed_number_of_students:
		message = "ظرفیت این درس پر شده است."
		request.session.flash(message)
		return HTTPFound(request.route_url('select_courses'))

	selected_courses = request.dbsession.query(SelectedCourses
		).filter_by(student=student).all()

	credits = 0
	for s in selected_courses:
		credits += s.course.credits

	# use session to store message
	if (credits + course.credits) > MAX_CREDITS:
		message = "حد مجاز برای انتخاب واحد رعایت نشده است."
		request.session.flash(message)
		return HTTPFound(request.route_url('select_courses'))

	# add the course
	SelectedCourses(student=student, course=course)

	# a student took the course
	course.signed_up_students += 1

	return HTTPFound(request.route_url('select_courses'))



@view_config(route_name='drop_course',
             renderer='string')
def drop_course(request):
	user = request.user
	student = request.dbsession.query(Student).filter_by(user=user).first()

	course_id = int(request.matchdict.get('id', -1))
	course = request.dbsession.query(Course).filter_by(id=course_id).first()

	# delete the course
	selected_course = request.dbsession.query(SelectedCourses).filter_by(
		student=student, course=course)

	# a student dropped the course
	selected_course.first().course.signed_up_students -= 1
	selected_course.delete()

	return HTTPFound(request.route_url('select_courses'))
