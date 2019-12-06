from typing import List, Dict

class Course:
    """
    ===Description===
    A course object containing all relevant information about a current course for the school year

    ==Assumptions==
    A valid course_file path is given
    No information is lacking in the .json files

    ==Representation Invariants==
    len(course_data) == 13
    """
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
    _meeting_sections: Dict
    _num_valid_course_comb: int
    _lectures_list: List
    _tutorials_list: List

    def __init__(self, id: str, code: str, name: str, description: str, department: str, division: str,
                 prerequisites: str, exclusions: str, level: str,
                 campus: str, term: str, breadths: List[int], meeting_section: Dict) -> None:
        self._id = id
        self._code = code
        self._name = name
        self._description = description
        self._division = department
        self._department = division
        self._prerequisites = prerequisites
        self._exclusions = exclusions
        self._level = level
        self._campus = campus
        self._term = term
        self._breadths = breadths
        self._meeting_section = meeting_section

    def get_id(self) -> str:
        """Returns the id of the course"""
        return self._id

    def get_code(self) -> str:
        """Returns the course code"""
        return self._code

    def get_name(self) -> str:
        """Returns the name of the course"""
        return self._name

    def get_description(self) -> str:
        """Returns the description of the course"""
        return self._description

    def get_division(self) -> str:
        """Returns the division of the course"""
        return self._division

    def get_semester(self) -> str:
        """Returns the semester of the course as F, S or Y"""
        if "H5S" in self.get_code():
            return "S"
        if "H5F" in self.get_code():
            return "F"
        return "Y"

    def get_prerequisites(self) -> str:
        """Returns the prerequisites for the course"""
        return self._prerequisites

    def get_exclusions(self) -> str:
        """Returns the exclusions for the course"""
        return self._exclusions

    def get_level(self) -> int:
        """Returns the level of the course"""
        return self._level

    def get_campus(self) -> str:
        """Returns the campus of where the course is located in (UTSC, UTM, UTSG)"""
        return self._campus

    def get_breadths(self) -> List[int]:
        """Returns the breadths of the course"""
        return self._breadths

    def get_meeting_section(self) -> List[Dict]:
        """Returns the section for the course"""
        return self._meeting_section

    def get_meeting_section_codes(self) -> List[str]:
        """Returns all the codes for all section of the course"""
        return self._meeting_section["code"]

    def get_meeting_section_instructors(self) -> List[str]:
        """Returns all the instructors for all section of the course"""
        return [section["instructors"] for section in self._meeting_section]

    def get_meeting_section_times(self) -> List[Dict]:
        """Returns the time for the section of the course"""
        # lst = []
        # for section in self._meeting_sections:
        #     lst.extend(section['times'])
        # return lst
        return self._meeting_section['times']

    def get_meeting_section_size(self) -> List[str]:
        """Returns all the sizes for the section of the course"""
        return [section["size"] for section in self._meeting_section]

    def get_meeting_section_enrolment(self) -> List[str]:
        """Returns all the enrolment sizes for the section of the course"""
        return [section["enrolment"] for section in self._meeting_section]

# a = Course("another_one/CSC236H5F20199.json")
# ========Extraction of data complete========
# print(a.get_id())
# print(a.get_code())
# print(a.get_name())
# print(a.get_description())
# print(a.get_division())
# print(a.get_prerequisites())
# print(a.get_exclusions())
# print(a.get_level())
# print(a.get_campus())
# print(a.get_breadths())
# print(a.get_meeting_section())
# print(a.get_meeting_section_codes())
# print(a.get_meeting_section_instructors())
# print(a.get_meeting_section_times())
# print(a.get_meeting_section_size())
# print(a.get_meeting_section_enrolment())


# a = Course("another_one/CSC236H5F20199.json")
# print(a.get_lectures_list())
# print(a.get_tutorials_practicals_list())
# for i in a.get_lectures_list():
#     print(i)
# for i in a.get_tutorials_practicals_list():
#     print(i)
# a.get_valid_course_combination()
