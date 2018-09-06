from .views.user import get_user


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    
    # show courses
    config.add_route('courses', '/course/')
    config.add_route('select_courses', '/select_courses/')
    # add course
    config.add_route('add_course', '/add_course/{id}')
    # remove course
    config.add_route('drop_course', '/drop_course/{id}')

    # show student information
    config.add_route('student_information', '/student_information')
    
    # edit student information
    config.add_route('edit_student_information', '/edit_student_information')
    config.add_route('update_student_information', '/update_student_information')
    

    # login, logout
    config.add_route('auth', '/sign/{action}')

	# make request.user accessible in views and templates    
    config.add_request_method(get_user, 'user', reify=True)
