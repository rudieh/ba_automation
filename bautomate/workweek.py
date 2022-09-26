from typing import List
from bautomate.workday import WorkDay

class WorkWeek():
    """
    Class representing one work week.

    Properties:
        days:       List of WorkDays.
    """
    def __init__(self, **kwargs):
        self.days = kwargs.get("days", [])

    def __str__(self):
        s = ""
        for k in self.__dict__.keys():
            s += '\n'
            s += f'{k}: {getattr(self, k)}'
        return s

    def __repr__(self):
        s = ""
        for k in self.__dict__.keys():
            s += '\n'
            s += f'{k}: {getattr(self, k)}'
        return s

    @property
    def days(self) -> List:
        """List of work blocks/hours of this day."""
        return self._days

    @days.setter
    def days(self, k: List) -> None:
        if not isinstance(k, List):
            raise TypeError

        if not hasattr(self, "_days"):
            self._days = []

        for e in k:
            self._days.append(WorkDay(**e))