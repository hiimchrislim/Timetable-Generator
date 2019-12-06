from typing import List, Dict
from course import Course
import itertools
import json
from Filter import Filter


class CourseManager:
    """
    ==Description==
    A CourseManager containing all the courses before going into the Timetable
    """
    _courses_list: List
    _id: str
    _code: str
    _name: str
    _description: str
    _division: str
    _department: str
    _prerequisites: str
    _exclusions: str
    _level: int
    _campus: str
    _term: str
    _breadths: List[int]
    _meeting_sections: List[Dict]
    _lectures_list: List
    _tutorials_practicals_list: List
    _filter: Filter

    def __init__(self, course_file='', filter=Filter()) -> None:
        try:
            course_data = json.loads(open(course_file, "r").readline())
            self._id = course_data["id"]
            self._code = course_data["code"]
            self._name = course_data["name"]
            self._description = course_data["description"]
            self._division = course_data["division"]
            self._department = course_data["department"]
            self._prerequisites = course_data["prerequisites"]
            self._exclusions = course_data["exclusions"]
            self._level = course_data["level"]
            self._campus = course_data["campus"]
            self._term = course_data["term"]
            self._breadths = course_data["breadths"]
            self._meeting_sections = course_data["meeting_sections"]
            self._lectures_list = []
            self._tutorials_practicals_list = []
            self._filter = filter
            self.set_courses()

        except (FileNotFoundError):
            print("No valid file path given as it's not needed or a possible error occured.")

    def set_courses(self) -> None:
        for section in self._meeting_sections:
            # print(section) # Debugging only
            temp_lst = []
            if "T" not in section["code"][0] and "P" not in section["code"][0]:
                for time in section['times']:
                    temp_lst.append((self._filter.get_start_time() <= time['start'] <= self._filter.get_end_time()) \
                                    and (self._filter.get_start_time() <= time['end'] <= self._filter.get_end_time()) \
                                    and time['day'] not in self._filter.get_days_excluded() \
                                    and not (self._filter.get_lunch_time_start() <= time[
                        'start'] <= self._filter.get_lunch_time_end())
                                    and not (self._filter.get_lunch_time_start() <= time[
                        'end'] <= self._filter.get_lunch_time_end()))
                if all(temp_lst):
                    self._lectures_list.append(
                        Course(self._id, self._code, self._name, self._description, self._division, self._department,
                               self._prerequisites, self._exclusions, self._level, self._campus, self._term,
                               self._breadths, section))
            else:
                for time in section['times']:
                    temp_lst.append((self._filter.get_start_time() <= time['start'] <= self._filter.get_end_time()) \
                                    and (self._filter.get_start_time() <= time['end'] <= self._filter.get_end_time()) \
                                    and time['day'] not in self._filter.get_days_excluded() \
                                    and not (self._filter.get_lunch_time_start() <= time[
                        'start'] < self._filter.get_lunch_time_end())
                                    and not (
                            self._filter.get_lunch_time_start() < time['end'] < self._filter.get_lunch_time_end()))
                if all(temp_lst):
                    self._tutorials_practicals_list.append(
                        Course(self._id, self._code, self._name, self._description, self._division, self._department,
                               self._prerequisites, self._exclusions, self._level, self._campus, self._term,
                               self._breadths, section))

    def get_lectures_list(self) -> List:
        return self._lectures_list

    def get_tutorials_or_practical_list(self) -> List:
        return self._tutorials_practicals_list

    def get_valid_course_combination(self, c1: list, c2: list) -> list:
        """Returns all the valid course combinations for a tutorial/practical and lecture"""
        t1 = Timetable()
        if len(c1) == 0:
            return c2 if t1.add_course(self._break_down_nested_list(c2), self._filter) else []
        if len(c2) == 0:
            return c1 if t1.add_course(self._break_down_nested_list(c1), self._filter) else []
        all_courses = [c1] + [c2]
        all_course_combinations = list(itertools.product(*all_courses))
        valid_courses = []
        for combination in all_course_combinations:
            t = Timetable()
            # t._generate_empty_table()
            if t.add_course(self._break_down_nested_list(combination), self._filter):
                valid_courses.append(combination)
                # print("Timetable #: " + str(i))
                # i+= 1
        return valid_courses

    def _break_down_nested_list(self, nested_list: list) -> List:
        """Breaks down any nested list and will return a flattened list"""
        if isinstance(nested_list, Course):
            return [nested_list]
        else:
            s = list()
            for i in nested_list:
                s.extend(self._break_down_nested_list(i))
            return s


class Timetable:
    """
    ===Description===
    A timetable object representing the entire Timetable for the school year

    ===Representation Invariants===
    len(_first_semester_table) == 28
    len(_first_semester_table[n]) == 5 (where 0 < n < 28)
    """
    _first_semester_table: List[List]
    _second_semester_table: List[List]

    def __init__(self):
        self._first_semester_table = self._generate_empty_table()
        self._second_semester_table = self._generate_empty_table()

    def _generate_empty_table(self) -> List[List]:
        """Generates a 5 by 28 table where 8 am represents Index 0 and 21:30 represents Index 27"""
        lst = []
        for i in range(28):
            lst.append([None, None, None, None, None])
        return lst

    def get_first_semester_table(self) -> List[List]:
        """Returns the first semester table"""
        return self._first_semester_table

    def get_second_semester_table(self) -> List[List]:
        """Returns the second semester table"""
        return self._second_semester_table

    def add_course(self, courses: List[Course], filter=Filter()) -> bool:
        """Adds a course to the timetable
        This function returns True when the course was added successfully, False otherwise (when the timetable is
        occupied by another course)"""
        dates = {"MONDAY": 0, "TUESDAY": 1, "WEDNESDAY": 2, "THURSDAY": 3, "FRIDAY": 4}
        lectures = {"MONDAY": 0, "TUESDAY": 0, "WEDNESDAY": 0, "THURSDAY": 0, "FRIDAY": 0}
        tutorials_practicals = {"MONDAY": 0, "TUESDAY": 0, "WEDNESDAY": 0, "THURSDAY": 0, "FRIDAY": 0}
        # for course in courses:
        #     print(course.get_meeting_section())
        # print('-------')
        for course in courses:
            # print(course.get_meeting_section_times())
            for time in course.get_meeting_section_times():
                day_by_number = dates.get(time['day'])  # This will get you the value
                day = time['day']
                # ROUDING FIX 0.5 hours??
                # Get the difference from start time to beginning time then multiply by 2 (each half hour)
                start_time = (time['start'] // 3600 - 8) * 2
                end_time = (time['end'] // 3600 - 8) * 2
                # Ex. 9 am would be @ 1
                added_lectures = True
                added_tutorials_practicals = True
                if course.get_semester() == "F":
                    # First Semester Courses
                    for time_slot in range(start_time, end_time):
                        if self.get_first_semester_table()[time_slot][day_by_number] is None:
                            self.get_first_semester_table()[time_slot][day_by_number] = course
                            # print("Added " + str(course.get_code()) + " " + str(course.get_meeting_section_times()))
                            if "L" in course.get_meeting_section()['code']:
                                # print(course.get_meeting_section()['code'])
                                if added_lectures:
                                    lectures[day] += 1  # This will get you the key rather than the value
                                    added_lectures = False
                                    if lectures[day] > filter.get_maximum_lectures_per_day():
                                        return False
                            else:
                                if added_tutorials_practicals:
                                    tutorials_practicals[day] += 1
                                    added_tutorials_practicals = False
                                    if tutorials_practicals[day] > filter.get_maximum_tutorials_practicals_per_day():
                                        return False
                        else:
                            return False
                elif course.get_semester() == "S":
                    # Second Semester Courses
                    # print(time)
                    for time_slot in range(start_time, end_time):
                        if self.get_second_semester_table()[time_slot][day_by_number] is None:
                            self.get_second_semester_table()[time_slot][day_by_number] = course
                            if "L" in course.get_meeting_section()['code']:
                                # print(course.get_code())
                                # print(time)
                                # print(course.get_meeting_section())
                                if added_lectures:
                                    lectures[day] += 1  # This will get you the key rather than the value
                                    added_lectures = False
                                    if lectures[day] > filter.get_maximum_lectures_per_day():
                                        # print(lectures)
                                        # print(tutorials_practicals)
                                        # print("--------------------")
                                        return False
                            else:
                                if added_tutorials_practicals:
                                    tutorials_practicals[day] += 1
                                    added_tutorials_practicals = False
                                    if tutorials_practicals[day] > filter.get_maximum_tutorials_practicals_per_day():
                                        # print(lectures)
                                        # print(tutorials_practicals)
                                        # print("--------------------")
                                        return False
                        else:
                            # print(lectures)
                            # print(tutorials_practicals)
                            # print("--------------------")
                            return False
                else:
                    # Full Year Courses
                    for time_slot in range(start_time, end_time):
                        if self.get_second_semester_table()[time_slot][day] is None:
                            self.get_second_semester_table()[time_slot][day] = course.get_code()
                        else:
                            return False

        # for i in lectures:
        #     if lectures[i] > filter.get_maximum_lectures_per_day():
        #         return False
        # for h in tutorials_practicals:
        #     if tutorials_practicals[h] > filter.get_maximum_tutorials_practicals_per_day():
        #         return False
        # print(lectures)
        # print(tutorials_practicals)
        return True

# a = Timetable()
# print(a)

# cm = CourseManager("another_one/CSC236H5F20199.json")
# a = cm.get_valid_course_combination()
# cm = CourseManager("another_one/CSC207H5F20199.json")
# b = cm.get_valid_course_combination()
# t = Timetable()

# cm = CourseManager("another_one/CSC207H5F20199.json")
# print(len(cm.get_valid_course_combination()))
# cm = CourseManager("another_one/CSC290H5F20199.json")
# print(len(cm.get_valid_course_combination()))
# cm = CourseManager("another_one/CSC258H5S20201.json")
# print(len(cm.get_valid_course_combination()))
# cm = CourseManager("another_one/CSC263H5S20201.json")
# print(len(cm.get_valid_course_combination()))
# cm = CourseManager("another_one/CSC209H5S20201.json")
# print(len(cm.get_valid_course_combination()))
# cm = CourseManager("another_one/CCT111H5S20201.json")
# print(len(cm.get_valid_course_combination()))
# cm = CourseManager("another_one/MAT232H5F20199.json")
# print(len(cm.get_valid_course_combination()))
# cm = CourseManager("another_one/MAT224H5S20201.json")
# print(len(cm.get_valid_course_combination()))
# cm = CourseManager("another_one/MAT223H5F20199.json")
# print(len(cm.get_valid_course_combination()))

# for i in cm.get_valid_course_combination():
#     for g in i:
#         print(g.get_code())
#         print(g.get_meeting_section())
#     print("------------")
# u.add_course("CSC236H5F20199")
# u.add_course("CSC207H5F20199")
# u.add_course("CSC290H5F20199")
# u.add_course("CSC258H5S20201")
# u.add_course("CSC263H5S20201")
# u.add_course("CSC209H5S20201")
# u.add_course("CCT111H5S20201")
# u.add_course("MAT232H5F20199")
# u.add_course("MAT224H5F20199")
# u.add_course("MAT240H5S20201")
