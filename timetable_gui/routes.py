from flask import Flask, render_template, flash, redirect, url_for, request
from timetable_gui.config import Config
from timetable_gui.form import AddCourseForm
import pandas as pd
from Main import User
import random
from timetable import Timetable, CourseManager
import os

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
list_of_courses = set([])
days_excluded_fall = set([])
days_excluded_winter = set([])
courses_color = None
first_semester_max_courses = None
first_semester_tutorials_practicals = None
second_semester_max_courses = None
second_semester_tutorials_practicals = None
fall_start_time = 28800
fall_end_time = 28800
winter_start_time = 28800
winter_end_time = 28800
fall_lunch_start_time = 28800
fall_lunch_end_time = 28800
winter_lunch_start_time = 28800
winter_lunch_end_time = 28800
# seen_courses = {"MONDAY": [],
#                 "TUEDAY": [],
#                 "WEDNESDAY": [],
#                 "THURSDAY": [],
#                 "FRIDAY": []}
seen_courses = []
temp_dict = {"MONDAY": [{}, False], "TUESDAY": [{}, False], "WEDNESDAY": [{}, False], "THURSDAY": [{}, False],
             "FRIDAY": [{}, False]}


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = AddCourseForm()
    if form.validate_on_submit():
        if 'addCourse' in request.form:
            if form.course_textbox.data != '':
                # flash("Course: {}".format(form.course_textbox.data))
                list_of_courses.add(form.course_textbox.data)
        if 'removeCourse' in request.form:
            try:
                list_of_courses.remove(form.course_textbox.data)
            except(KeyError):
                print("Invalid Course Removal")
        if 'excludeDayFall' in request.form:
            days_excluded_fall.add(form.days_removal_textbox_fall.data)
        if 'excludeDayWinter' in request.form:
            days_excluded_winter.add(form.days_removal_textbox_winter.data)
    if 'removeDayFall' in request.form:
        try:
            days_excluded_fall.remove(form.days_removal_textbox_fall.data)
        except(KeyError):
            print("Invalid Day Removal")
    if 'removeDayWinter' in request.form:
        try:
            days_excluded_winter.remove(form.days_removal_textbox_winter.data)
        except(KeyError):
            print("Invalid Day Removal")
    if 'generateTimetable' in request.form:
        print('Generating...')
        print('Redirecting')
        global first_semester_max_courses, first_semester_tutorials_practicals, second_semester_max_courses, \
            second_semester_tutorials_practicals, fall_start_time, fall_end_time, winter_start_time, winter_end_time, \
            winter_lunch_start_time, winter_lunch_end_time, fall_lunch_start_time, fall_lunch_end_time
        first_semester_max_courses = int(request.form['fallMaxCourses'])
        first_semester_tutorials_practicals = int(request.form['fallMaxTutorialsPracticals'])
        second_semester_max_courses = int(request.form['winterMaxCourses'])
        second_semester_tutorials_practicals = int(request.form['winterMaxTutorialsPracticals'])
        fall_start_time = float(request.form['fallStartTime'])
        fall_end_time = float(request.form['fallEndTime'])
        winter_start_time = float(request.form['winterStartTime'])
        winter_end_time = float(request.form['winterEndTime'])
        winter_lunch_start_time = float(request.form['winterLunchStartTime'])
        winter_lunch_end_time = float(request.form['winterLunchEndTime'])
        fall_lunch_start_time = float(request.form['fallLunchStartTime'])
        fall_lunch_end_time = float(request.form['fallLunchEndTime'])
        return redirect(url_for('timetable'))
    return render_template('home.html', form=form, courses=list_of_courses, days_excluded_fall=days_excluded_fall,
                           days_excluded_winter=days_excluded_winter)


# df = pd.DataFrame({'A': [0, 1, 2, 3, 4], 'B': [5, 6, 7, 8, 9], 'C': ['a', 'b', 'c--', 'd', 'e']})


@app.route('/timetable', methods=['GET', 'POST'])
def timetable():
    u = User()
    for course in list_of_courses:
        if course + ".json" in os.listdir("/Users/chris/PycharmProjects/Timetable-Generator/another_one"):
            u.add_course(course)
    # global courses_color
    global courses_color
    courses_color = assign_color_to_courses()
    u.set_first_semester_filter((fall_start_time) * 3600, (fall_end_time) * 3600, days_excluded_fall,
                                fall_lunch_start_time, fall_lunch_end_time, first_semester_max_courses,
                                first_semester_tutorials_practicals)
    u.set_second_semester_filter((winter_start_time) * 3600, (winter_end_time) * 3600, days_excluded_winter,
                                 winter_lunch_start_time, winter_lunch_end_time, second_semester_max_courses,
                                 second_semester_tutorials_practicals)
    possible_timetables = u.get_valid_combinations()
    cm = CourseManager()
    fst = Timetable()
    # print(str(len(possible_timetables[0])) + " timetables generated")
    if len(possible_timetables[0]) != 0:
        fs = random.randint(0, (len(possible_timetables[0]) - 1))  # Can get a -1 error for no possible timetables
    else:
        fs = -1
    if len(possible_timetables[1]) != 0:
        ss = random.randint(0, (len(possible_timetables[1]) - 1))
    else:
        ss = -1
    # print(str(a) + " is the timetable picked")
    if fs != -1:
        fst.add_course(cm._break_down_nested_list(possible_timetables[0][fs]), u.get_first_semester_filter())
    if ss != -1:
        fst.add_course(cm._break_down_nested_list(possible_timetables[1][ss]), u.get_second_semester_filter())
    columns = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']
    index = ['8:00am', '8:30am', '9:00am', '9:30am', '10:00am', '10:30am',
             '11:00am', '11:30am', '12:00pm', '12:30pm',
             '1:00pm', '1:30pm', '2:00pm', '2:30pm',
             '3:00pm', '3:30pm', '4:00pm', '4:30pm',
             '5:00pm', '5:30pm', '6:00pm', '6:30pm',
             '7:00pm', '7:30pm', '8:00pm', '8:30pm',
             '9:00pm', '9:30pm']
    # print(t.get_first_semester_table())
    data_first_semester = fst.get_first_semester_table()
    data_second_semester = fst.get_second_semester_table()
    for i in range(len(data_first_semester)):
        for h in range(len(data_first_semester[i])):
            if data_first_semester[i][h] is None:
                data_first_semester[i][h] = ''
            else:
                data_first_semester[i][h] = str(
                    data_first_semester[i][h].get_code() + " " + data_first_semester[i][h].get_meeting_section_codes())
    for i in range(len(data_second_semester)):
        for h in range(len(data_second_semester[i])):
            if data_second_semester[i][h] is None:
                data_second_semester[i][h] = ''
            else:
                data_second_semester[i][h] = str(data_second_semester[i][h].get_code() + " " + data_second_semester[i][
                    h].get_meeting_section_codes())
    df1 = pd.DataFrame(data_first_semester, columns=columns,
                       index=index)
    th_props = [
        ('text-align', 'center'),
        ('color', '#6d6d6d'),
        ('background-color', '#f7f7f9')
    ]
    td_props = [
        ('font-size', '20px')
    ]
    styles = [dict(selector="tr", props=th_props),
              dict(selector="td", props=td_props)]
    # df1.style.applymap(highlight_courses)
    test = dict(selector="th", props=[('text-align', 'center')])
    df1.style.set_table_styles([test])
    df1.style.set_table_styles(styles).render()
    df2 = pd.DataFrame(data_second_semester, columns=columns, index=index)
    df2.style.set_table_styles([test])
    df2.style.set_table_styles(styles).render()
    # print(df2.style.render())
    # print(df1.style.render())
    for day, content in df1.iteritems():
        for item in content:
            if item != '':
                if item not in temp_dict[day]:
                    temp_dict[day][0][item] = False
    # print(temp_dict)
    # print(type(df1.iteritems()))
    # df1.to_html(border=0, escape=False)
    # print(courses_color)
    return render_template("timetable.html",
                           data_frame=df1.style.applymap(highlight_courses_background,
                                                      subset=columns).render(),
                           data_frame2=df2.style.applymap(highlight_courses_background, subset=columns).render())
# applymap(highlight_courses_background, subset='columns')


def assign_color_to_courses():
    temp_dict = {}
    colors = ['maroon', 'green', 'blue', 'red', 'orange', 'coral', 'teal', 'crimson',
              'gold', 'aqua', 'indigo']
    for course in list_of_courses:
        # print(course)
        temp_dict[course[:9]] = colors[random.randint(0, len(colors) - 1)]
    return temp_dict


def highlight_courses_background(value):
    # print(courses_color)
    if value.split(" ")[0] in courses_color:
        return 'background-color: %s' % courses_color[value.split(" ")[0]]
    return ''


def highlight_courses_text(value):
    # global temp_dict
    # current_day = None
    # for day in temp_dict:
    #     if temp_dict[day][1] is False:
    #         current_day = day
    #         break
    print(value)
    print(temp_dict)
    # if value != '':
    #     if value not in seen_courses:
    #         seen_courses.append(value)
    #         return 'color: white'
    #     else:
    #         return 'color: %s' % 'green'
    # return 'color: black'
    # if value in temp_dict[current_day][0]:
    #     if temp_dict[current_day][0][value] == False:
    #         # print('Returning White')
    #         temp_dict[current_day][0][value] = True
    #         print('white')
    #         print('-----')
    #         return 'color: white'
    #         # print('Returning Course Color')
    #         # return 'color: %s' % color
    #     else:
    #         color = courses_color[value.split(" ")[0]]
    #         print(color)
    #         print('-----')
    #         return "color: %s" % str(color)
    # print('white')
    # print('-----')
    # return 'color: white'
    #-------------------------
    # if value not in seen_courses[current_day] and value != '':
    #     seen_courses[current_day].append(value)
    #     return 'color: white'
    # elif value in seen_courses:
    #     return 'color: %s' % courses_color[value.split(" ")[0]]
    # desc = df.describe(include='all')

    # return render_template('timetable.html', tables=[df.to_html(classes='data')], titles=df.columns.values)
    # return render_template('timetable.html', data_frame=df.to_html(classes='data', header='true'), stat=desc.to_html())
