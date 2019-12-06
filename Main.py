from timetable import Timetable, CourseManager
from typing import List
import itertools
from Filter import Filter


class Stack:
    """
    ===Description===
    A stack class used through a list implementation. The top of the stack is the end of the list

    ==Representation Invariants==
    len(self._s) >= 0
    """
    _s: List

    def __init__(self):
        self._s = []

    def is_empty(self) -> bool:
        """Returns True is the stack is empty, false otherwise"""
        return len(self._s) == 0

    def pop(self) -> any:
        """Returns the item at the top of the stack (last item in the list)"""
        return self._s.pop()

    def push(self, item: any) -> None:
        """Pushes an item to the top of the stack"""
        self._s.append(item)


class TimetableManager:
    """
    ===Description===
    A Timetable Manager which contains all of the possible Timetables for the specific courses picked

    ===Representation Invariants===
    len(all_possible_timetables) <= 0
    """
    all_valid_timetables: List[Timetable]

    def __init__(self):
        self.all_valid_timetables = []

    def add_timetable(self, timetable: Timetable) -> None:
        """Adds the timetable to the list of all possible timetables"""
        self.all_valid_timetables.append(timetable)

    def amount_of_timetables(self) -> int:
        """Returns the amount of timetables generated"""
        return len(self.all_valid_timetables)

    def get_all_timetables(self) -> List[Timetable]:
        """Returns all the valid timetables generated"""
        return self.all_valid_timetables


class User:
    """
    ===Description===
    A User object to create Timetables for the user
    """
    _tm: TimetableManager
    _name: str
    _studentId: str
    _studentNumber: int
    _courses: list
    _first_semester_filter: Filter
    _second_semester_filter: Filter

    # _f_courses: List
    # _s_courses: List
    # _first_semester_courses: List
    # _second_semester_courses: List

    def __init__(self, name="student", studentId="abcdefgh", studentNumber=1234567890):
        self._tm = TimetableManager()
        self._name = name
        self._studentId = studentId
        self._studentNumber = studentNumber
        # self._f_courses = []
        # self._s_courses = []
        # self._first_semester_courses = []
        # self._second_semester_courses = []
        self._courses = []
        self._first_semester_filter = None
        self._second_semester_filter = None

    def add_course(self, course_name) -> None:
        self._courses.append("/Users/chris/PycharmProjects/Timetable-Generator/another_one/" + course_name + ".json")

        # "/Users/chris/PycharmProjects/Timetable-Generator/another_one/"
        # "/Users/chris/PycharmProjects/Timetable-Generator/lets_a_go/"
        # == Original concept below ==
        # if "H5F" in course_name:
        #     self._f_courses.append("another_one/" + course_name + ".json")
        #     self._first_semester_courses.append(self._get_valid_combinations())
        # elif "H5S" in course_name:
        #     self._s_courses.append("another_one/" + course_name + ".json")
        #     self._second_semester_courses(self._get_valid_combinations())
        # else:
        #     # Put it in both _f_courses and _s_courses
        #     print("H5Y Not Implemented Yet")

    # def set_valid_timetables(self, valid_combinations: list):
    #     cm = CourseManager()
    #     for valid_timetable in self.get_valid_combinations():
    #         print(valid_timetable)
    # self._tm.add_timetable(Timetable().add_course(valid_timetable))

    # def get_valid_timetables(self) -> list:

    def get_valid_combinations(self) -> tuple:
        first_semester_s = Stack()
        second_semester_s = Stack()
        first_sem_total_classes = 0 # Keeps track of all possible courses regardless tutorials/practicals to make sure
        #  that you don't get a semester with less classes than you wanted (i.e Adding 3 courses but only getting
        # a schedule with 2 courses
        second_sem_total_classes = 0
        for course in self._courses:
            if "H5F" in course and self.has_set_first_semester_filter():
                cm = CourseManager(course, self.get_first_semester_filter())
                first_semester_s.push(
                    cm.get_valid_course_combination(cm.get_lectures_list(), cm.get_tutorials_or_practical_list()))
                first_sem_total_classes += 1
                if cm.get_tutorials_or_practical_list() is not []:
                    first_sem_total_classes += 1
            elif "H5S" in course and self.has_set_second_semester_filter():
                cm = CourseManager(course, self.get_second_semester_filter())
                second_semester_s.push(
                    cm.get_valid_course_combination(cm.get_lectures_list(), cm.get_tutorials_or_practical_list()))
                second_sem_total_classes += 1
                if cm.get_tutorials_or_practical_list() is not []:
                    second_sem_total_classes += 1
            else:
                cm = CourseManager(course)
                first_semester_s.push(
                    cm.get_valid_course_combination(cm.get_lectures_list(), cm.get_tutorials_or_practical_list()))
                second_semester_s.push(
                    cm.get_valid_course_combination(cm.get_lectures_list(), cm.get_tutorials_or_practical_list()))

        while not first_semester_s.is_empty():
            first_course = first_semester_s.pop()
            if not first_semester_s.is_empty():
                second_course = first_semester_s.pop()
                first_semester_s.push(cm.get_valid_course_combination(first_course, second_course))
            else:
                # return cm._break_down_nested_list(first_course)
                first_semester_s.push(first_course)
                break

        while not second_semester_s.is_empty():
            first_course = second_semester_s.pop()
            if not second_semester_s.is_empty():
                second_course = second_semester_s.pop()
                second_semester_s.push(cm.get_valid_course_combination(first_course, second_course))
            else:
                second_semester_s.push(first_course)
                break

        if not first_semester_s.is_empty():
            f = first_semester_s.pop()
            if len(cm._break_down_nested_list(f)) < first_sem_total_classes:
                f = []
        else:
            f = []
        if not second_semester_s.is_empty():
            s = second_semester_s.pop()
            if len(cm._break_down_nested_list(s)) < second_sem_total_classes:
                s = []
        else:
            s = []
        # if f == [] and s == []:
        #     return []
        # return CourseManager().get_valid_course_combination(f, s)
        return f, s

    def set_first_semester_filter(self, start: int, end: int, days_excluded: list, lunch_time_start: int,
                                  lunch_time_end: int, maximum_lectures_per_day: int,
                                  maximum_tutorials_practicals_per_day: int):
        self._first_semester_filter = Filter(start, end, days_excluded, lunch_time_start, lunch_time_end,
                                             maximum_lectures_per_day, maximum_tutorials_practicals_per_day)

    def set_second_semester_filter(self, start: int, end: int, days_excluded: list, lunch_time_start: int,
                                   lunch_time_end: int, maximum_lectures_per_day: int,
                                   maximum_tutorials_practicals_per_day: int):
        self._second_semester_filter = Filter(start, end, days_excluded, lunch_time_start, lunch_time_end,
                                              maximum_lectures_per_day, maximum_tutorials_practicals_per_day)

    def get_first_semester_filter(self) -> Filter:
        return self._first_semester_filter

    def get_second_semester_filter(self) -> Filter:
        return self._second_semester_filter

    def has_set_first_semester_filter(self) -> bool:
        return self._first_semester_filter is not None

    def has_set_second_semester_filter(self) -> bool:
        return self._second_semester_filter is not None

    # == Original concept below ==
    # for course in self._f_courses:
    #     cm = CourseManager(course)
    #
    #     # self._first_semester_courses.append(cm.get_lectures_list())
    #     # self._first_semester_courses.append(cm.get_tutorials_or_practical_list())
    #     # self._first_semester_courses.append([])
    # # print(self._first_semester_courses)
    #
    # for course in self._s_courses:
    #     cm = CourseManager(course)
    #     self._second_semester_courses.append(cm.get_lectures_list())
    #     self._second_semester_courses.append(cm.get_tutorials_or_practical_list())
    # # print(self._second_semester_courses)
    # combinations = self._first_semester_courses + self._second_semester_courses
    # # print(self._first_semester_courses)
    # # print(self._second_semester_courses)
    # # combinations.remove([]) # Omitting empty semesters
    # # print(combinations)
    # return list(itertools.product(*combinations))
    # # print(a)

#
if __name__ == "__main__":
#     # tm = TimetableManager()
    u = User()
    # u.add_course("AST201H5S20201")
    # u.add_course("CSC258H5S20201")
    # u.add_course("CSC209H5S20201")
    # u.add_course("MAT224H5S20201")
    # u.add_course("CSC263H5S20201")

    u.add_course("CSC236H5F20199")
    u.add_course("CSC207H5F20199")
    u.add_course("CSC290H5F20199")
    u.add_course("MAT232H5F20199")
    u.add_course("MAT223H5F20199")
    #
    u.set_first_semester_filter((8) * 3600, (12 + 10) * 3600, [], 0, 0, 10, 10)
    # u.set_first_semester_filter((9) * 3600, (12 + 8) * 3600, ['WEDNESDAY','FRIDAY'], 61200, 68400, 3,2)
    u.set_second_semester_filter((8) * 3600, (12 + 5) * 3600, ['FRIDAY'], 18*3600, 19*3600, 3, 3)
#     # print(u.set_valid_timetables(u.get_valid_combinations()))
#     # print(len(u.get_valid_combinations()))
    a = u.get_valid_combinations()
    print(len(a[0]), len(a[1]))
#     # print(len(a[0]) * len(a[1]))
    for h in range(0, 1):
        try:
            # Sampling
            cm = CourseManager()
            for i in cm._break_down_nested_list(a[0][h]):
                print(i.get_code())
                print(i.get_meeting_section())
            # =====Testing Purposes=====
            t = TimetableManager()
            f = Timetable()
            for i in cm._break_down_nested_list(a[0][0]):
                f.add_course([i], u.get_first_semester_filter())
            print(f.get_first_semester_table())
            print(f.get_second_semester_table())
        except (IndexError):
            print("No Solutions Found")
#
# print(len(u._get_combinations()))
# for i in u._get_combinations():
#     for b in i:
#         print(b._get_meeting_section())
#     print("----------------")
# print(u._second_semester_courses)
# print(u._first_semester_courses[0].get_meeting_sections())
# print(u.get_combinations())

# Visual aspect - Set a color for each subject and make the timetables that have the colors in the blocks?
# TODO: Add full year course support (Later)
# TODO: When you add courses, make a new function to only generate valid combinations for first sem and second sem separately
