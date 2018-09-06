from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    UnicodeText,
    UniqueConstraint,
    DateTime,
    ForeignKey,
)

from .meta import Base
from sqlalchemy.orm import relationship
from .user import User


class Major(Base):
    __tablename__ = 'majors'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255))

    __table_args__ = (
        UniqueConstraint(name),
    )



# Course Model
class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255))
    credits= Column(Integer)    
    allowed_number_of_students = Column(Integer)
    signed_up_students = Column(Integer, default=0)
    exam_date = Column(DateTime)
    credits = Column(Integer)

    major_id = Column(
        Integer,
        ForeignKey('majors.id', ondelete='CASCADE'),
        nullable=False
    )
    major = relationship('Major', backref='courses')
    
    teacher_id = Column(
        Integer,
        ForeignKey('teachers.id', ondelete='CASCADE'),
        nullable=False
    )
    teacher = relationship('Teacher')
    

    __table_args__ = (
        UniqueConstraint(name),
    )



# Teacher Model
class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    user = relationship('User', backref='teachers')



# Student Model
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)

    major_id = Column(
        Integer,
        ForeignKey('majors.id', ondelete='CASCADE'),
        nullable=False
    )
    major = relationship('Major')


    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    user = relationship('User', backref='students')



# Student Model
class SelectedCourses(Base):
    __tablename__ = 'selected_courses'

    id = Column(Integer, primary_key=True)

    student_id = Column(
        Integer,
        ForeignKey('students.id', ondelete='CASCADE'),
        nullable=False,
    )
    student = relationship('Student', backref='students')

    course_id = Column(
        Integer,
        ForeignKey('courses.id', ondelete='CASCADE'),
    )
    course = relationship('Course')
