from typing import List


class Filter:
    """
    ===Description===
    This filter represents the constraints to generate a timetable to your liking.
    By default the start time will be at 8 and the end time will be at 9:30

    ===Representation Invariants===
    28800 <= start_time <= 77400
    28800 <= end_time <= 77400
    """
    _start_time: int
    _end_time: int
    _days_excluded: List[str]
    _lunch_time_start: int
    _lunch_time_end: int

    def __init__(self, start_time=28800, end_time=77400, days_excluded=[], lunch_time_start=43200, lunch_time_end=46800,
                 maximum_lectures_per_day=2, maximum_tutorials_practicals_per_day=2):
        self._start_time = start_time
        self._end_time = end_time
        self._days_excluded = days_excluded
        self._lunch_time_start = lunch_time_start
        self._lunch_time_end = lunch_time_end
        self.maximum_lectures_per_day = maximum_lectures_per_day
        self.maximum_tutorials_practicals_per_day = maximum_tutorials_practicals_per_day

    def get_maximum_lectures_per_day(self) -> int:
        """Returns the maximum number of lectures per day """
        return self.maximum_lectures_per_day

    def get_maximum_tutorials_practicals_per_day(self) -> int:
        """Returns the maximum number of tutorials/practicals per day"""
        return self.maximum_tutorials_practicals_per_day

    def get_start_time(self) -> int:
        """Returns the start time of the day"""
        return self._start_time

    def get_end_time(self) -> int:
        """Returns the end time of the day"""
        return self._end_time

    def get_days_excluded(self) -> List[str]:
        """Returns the days excluded"""
        return self._days_excluded

    def get_lunch_time_start(self) -> int:
        """Returns the time of when lunch starts"""
        return self._lunch_time_start

    def get_lunch_time_end(self) -> int:
        """Returns the time of when lunch ends"""
        return self._lunch_time_end
