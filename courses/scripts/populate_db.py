import os
import sys
import transaction
from datetime import datetime 
from random import randint

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )


from ..models.courses import Student, Teacher, Course, Major
from ..models.user import User


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    majors = [
        dict(name='فناوری اطلاعات'),
        dict(name='نرم افزار'),
        dict(name='سخت افزار'),
        dict(name='مدیریت')
    ]

    students = [
        # default: we use student id as username
        # and personal code as password
        # when student logged in the website he/she can edit the information
        dict(id=961111, firstname='مریم', lastname='امینی', personal_code='12121212', address='تهران', email='amin@example.com', phone='09301231234', birthday=datetime(2000, 8, 13)),
        dict(id=961122, firstname='زهرا', lastname='علوی', personal_code='14141414', address='اصفهان', email='ali@example.com', phone='09301241236', birthday=datetime(1995, 4, 21)),
        dict(id=942133, firstname='رضا', lastname='کریمی', personal_code='13131313', address='مشهد', email='reza@example.com', phone='09304251534', birthday=datetime(1996, 10, 22)),
        dict(id=942144, firstname='علی', lastname='حسنی', personal_code='19191919', address='قم', email='hamid@example.com', phone='09722515320', birthday=datetime(1995, 11, 3)),
        dict(id=953155, firstname='محمد', lastname='رضایی', personal_code='16161616', address='تهران', email='mohammad@example.com', phone='09010234434', birthday=datetime(1997, 6, 2)),
        dict(id=963166, firstname='فاطمه', lastname='محمدی', personal_code='23232323', address='آبادان', email='amir@example.com', phone='09114242521', birthday=datetime(1998, 10, 26)),
        dict(id=934177, firstname='مرضیه', lastname='امیدی', personal_code='43434343', address='تهران', email='reza@example.com', phone='09023041535', birthday=datetime(1999, 11, 11)),
        dict(id=964244, firstname='زهرا', lastname='نوایی', personal_code='62626262', address='اهواز', email='zahra@example.com', phone='09333042516', birthday=datetime(1997, 12, 12)),
        dict(id=955188, firstname='امید', lastname='حمیدی', personal_code='41414141', address='مشهد', email='omidamin@example.com', phone='09343042514', birthday=datetime(1992, 10, 2)),
        dict(id=925199, firstname='مینو', lastname='کریمی', personal_code='28282828', address='شیراز', email='mino@example.com', phone='09354251534', birthday=datetime(1994, 11, 12)),
        dict(id=946211, firstname='نرگس', lastname='امینی', personal_code='36363636', address='اصفهان', email='hasan@example.com', phone='09374251534', birthday=datetime(1997, 7, 3)),
        dict(id=956255, firstname='زینب', lastname='محمدی', personal_code='18181818', address='تهران', email='zeinab@example.com', phone='09314251534', birthday=datetime(2000, 1, 5)),
        dict(id=947266, firstname='فاطمه', lastname='امینی', personal_code='52525252', address='قم', email='fatemeh@example.com', phone='09304251534', birthday=datetime(1999, 6, 1)),
        dict(id=927222, firstname='رباب', lastname='هاشمی', personal_code='35353535', address='تهران', email='naqi@example.com', phone='09304251534', birthday=datetime(1993, 9, 13)),
        dict(id=938233, firstname='مریم', lastname='امیری', personal_code='15151515', address='زنجان', email='maryamamin@example.com', phone='09242897344', birthday=datetime(1993, 1, 1)),
        dict(id=958344, firstname='مهرنوش', lastname='فاطمی', personal_code='17171717', address='مشهد', email='mehrnoosh@example.com', phone='09310142514', birthday=datetime(1995, 12, 13)),
    ]

    courses = [
        dict(id=111111, name='مقدمات برنامه نویسی', credits=3, teacher=1, major=0, allowed_number_of_students=28, exam_date=datetime(2018, 5, 1)),
        dict(id=111222, name='شبکه ۱', credits=3, teacher=0, major=0, allowed_number_of_students=30, exam_date=datetime(2018, 5, 22)),
        dict(id=111333, name='شبکه ۲', credits=3, teacher=0, major=0, allowed_number_of_students=30, exam_date=datetime(2018, 4, 30)),
        dict(id=222333, name='کارگاه شبکه ۱', credits=1, teacher=0, major=1, allowed_number_of_students=10, exam_date=datetime(2018, 5, 6)),
        dict(id=222444, name='کارگاه شبکه ۲', credits=1, teacher=0, major=0, allowed_number_of_students=10, exam_date=datetime(2018, 5, 8)),
        dict(id=111444, name='مدیریت در فناوری اطلاعات', credits=3, teacher=3, major=0, allowed_number_of_students=25, exam_date=datetime(2018, 5, 12)),
        dict(id=111666, name='برنامه نویسی پیشرفته ۱', credits=3, teacher=1, major=1, allowed_number_of_students=30, exam_date=datetime(2018, 5, 8)),
        dict(id=111777, name='برنامه نویسی پیشرفته ۲', credits=3, teacher=1, major=0, allowed_number_of_students=30, exam_date=datetime(2018, 4, 30)),
        dict(id=111888, name='طراحی صفحات وب', credits=3, teacher=1, major=1, allowed_number_of_students=30, exam_date=datetime(2018, 4, 28)),
        dict(id=111999, name='هوش مصنوعی', credits=3, teacher=2, major=2, allowed_number_of_students=30, exam_date=datetime(2018, 5, 22)),
        dict(id=222111, name='طراحی الگوریتم', credits=3, teacher=1, major=2, allowed_number_of_students=30, exam_date=datetime(2018, 5, 12)),
        dict(id=222555, name='سیستم عامل', credits=3, teacher=2, major=1, allowed_number_of_students=30, exam_date=datetime(2018, 5, 12)),
        dict(id=222666, name='کارگاه سیستم عامل', credits=1, teacher=2, major=1, allowed_number_of_students=10, exam_date=datetime(2018, 5, 16)),
        dict(id=222777, name='مبانی مدیریت', credits=2, teacher=3, major=3, allowed_number_of_students=30, exam_date=datetime(2018, 5, 20)),
        dict(id=222888, name='گرافیک', credits=2, teacher=1, major=0, allowed_number_of_students=30, exam_date=datetime(2018, 5, 11)),
        dict(id=222999, name='ساختمان داده', credits=3, teacher=1, major=2, allowed_number_of_students=30, exam_date=datetime(2018, 5, 21)),
        dict(id=333111, name='کنترل پروژه', credits=3, teacher=4, major=3, allowed_number_of_students=36, exam_date=datetime(2018, 5, 19)),
        dict(id=333222, name='استاتیک', credits=3, teacher=4, major=3, allowed_number_of_students=30, exam_date=datetime(2018, 5, 6)),
        dict(id=333444, name='مدیریت سازمان ها', credits=3, teacher=3, major=3, allowed_number_of_students=30, exam_date=datetime(2018, 5, 1)),
        dict(id=333555, name='مقدمات مدیریت سازمان ها', credits=3, teacher=3, major=3, allowed_number_of_students=30, exam_date=datetime(2018, 5, 3)),
        dict(id=333666, name='کارگاه برنامه نویسی', credits=1, teacher=1, major=1, allowed_number_of_students=10, exam_date=datetime(2018, 5, 7)),
        dict(id=333777, name='رباتیک', credits=3, teacher=2, major=2, allowed_number_of_students=30, exam_date=datetime(2018, 5, 9)),
        dict(id=333888, name='سخت افزار', credits=3, teacher=2, major=2, allowed_number_of_students=30, exam_date=datetime(2018, 5, 25)),
        dict(id=333999, name='الکترونیک', credits=3, teacher=2, major=1, allowed_number_of_students=30, exam_date=datetime(2018, 5, 18)),
        dict(id=444111, name='آشنایی با پردازنده', credits=3, teacher=1, major=2, allowed_number_of_students=30, exam_date=datetime(2018, 5, 16)),
        dict(id=444222, name='ریاضی عمومی ۱', credits=3, teacher=4, major=0, allowed_number_of_students=36, exam_date=datetime(2018, 5, 19)),
        dict(id=444333, name='ریاضی عمومی ۲', credits=3, teacher=4, major=0, allowed_number_of_students=31, exam_date=datetime(2018, 5, 6)),
        dict(id=444555, name='فیزیک عمومی ۱', credits=3, teacher=3, major=1, allowed_number_of_students=33, exam_date=datetime(2018, 5, 1)),
        dict(id=444666, name='فیزیک عمومی ۲', credits=3, teacher=3, major=1, allowed_number_of_students=30, exam_date=datetime(2018, 5, 3)),
        dict(id=444777, name='اقتصاد مهندسی', credits=1, teacher=1, major=0, allowed_number_of_students=10, exam_date=datetime(2018, 5, 7)),
        dict(id=444888, name='ریاضی مهندسی', credits=3, teacher=2, major=1, allowed_number_of_students=30, exam_date=datetime(2018, 5, 9)),
        dict(id=444999, name='آمار و احتمال', credits=3, teacher=2, major=1, allowed_number_of_students=20, exam_date=datetime(2018, 5, 25)),
        dict(id=555111, name='مدار منطقی', credits=3, teacher=2, major=0, allowed_number_of_students=27, exam_date=datetime(2018, 5, 18)),
        dict(id=555222, name='معماری کامپیوتر', credits=3, teacher=1, major=2, allowed_number_of_students=30, exam_date=datetime(2018, 5, 16)),
    ]


    teachers = [
        # it, software, hardware
        dict(id=11244, firstname='نرگس', lastname='نوایی', personal_code='979797', address='اصفهان', email="narges01@gmail.com", phone='09310142522', birthday=datetime(1980, 12, 1)),
        dict(id=22244, firstname='علی', lastname='امینی', personal_code='969696', address='تهران', email="ali23@gmail.com", phone='09310142533', birthday=datetime(1966, 1, 18)),
        dict(id=33344, firstname='فاطمه', lastname='امیری', personal_code='959595', address='تهران', email="feteme34@gmail.com", phone='09310142544', birthday=datetime(1989, 10, 21)),

        # management
        dict(id=44244, firstname='رضا', lastname='محمدی', personal_code='949494', address='اصفهان', email="reza44@yahoo.com", phone='09310142555', birthday=datetime(1985, 5, 29)),
        dict(id=55344, firstname='امید', lastname='فاطمی', personal_code='939393', address='مشهد', email="omid882@gmail.com", phone='09310142566', birthday=datetime(1975, 2, 14)),
    ]


    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        students_query = []
        teachers_query = []
        courses_query = []
        majors_query = []

        for m in majors:
            major = Major(**m)
            dbsession.add(major)
            dbsession.flush()
            majors_query.append(major)

        for s in students:
            student_id = s.pop('id')
            user = User(**s, name=student_id, password="")
            user.set_password(user.personal_code)
            dbsession.add(user)
            dbsession.flush()
            student = Student(id=student_id, user=user,
                major=majors_query[randint(0, len(majors)-1)])
            dbsession.add(student)
            dbsession.flush()
            students_query.append(student)
    
        for t in teachers:
            teacher_id = t.pop('id')
            user = User(**t, name=teacher_id, password="")
            user.set_password(user.personal_code)
            dbsession.add(user)
            dbsession.flush()
            teacher = Teacher(id=teacher_id, user=user)
            dbsession.add(teacher)
            dbsession.flush()
            teachers_query.append(teacher)

        for c in courses:
            teacher = c.pop('teacher')
            major = c.pop('major')
            course = Course(**c, teacher=teachers_query[teacher], major=majors_query[major])
            dbsession.add(course)
            dbsession.flush()
