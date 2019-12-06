from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from typing import List


class AddCourseForm(FlaskForm):

        course_textbox = StringField('', validators=[])
        # DataRequired()
        days_removal_textbox_fall = StringField('', validators=[])
        days_removal_textbox_winter = StringField('', validators=[])

        # add_course_button = SubmitField('Add Course')
        # generate_timetables_button = SubmitField('Generate Timetables')
        # first_semester_courses = []
        # second_semester_courses = []
        # courses = ['a', 'b', 'c', 'd', 'e']

    # def get_course_textbox(self) -> StringField:
    #     """Returns the textbox where you add all your courses in"""
    #     return self.course_textbox
    #
    # def get_add_course_button(self) -> SubmitField:
    #     """Returns the button to add your course"""
    #     return self.addCourse_button
    #
    # def get_generate_timetables_button(self) -> SubmitField:
    #     """Returns the button to generate your timetables"""
    #     return self.generate_timetables_button
    #
    # def add_course(self, course: str) -> None:
    #     """Adds course to the list of courses sorted by first semester or second semester"""
    #     if "H5F" in course:
    #         self.first_semester_courses.append(course)
    #     else:
    #         self.second_semester_courses.append(course)
    #
    # def get_first_semester_courses(self) -> List[str]:
    #     """Returns all first semester courses added"""
    #     return self.first_semester_courses
    #
    # def get_second_semester_courses(self) -> List[str]:
    #     """Returns all the second semester courses added"""
    #     return self.second_semester_courses
