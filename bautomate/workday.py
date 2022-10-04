from typing import List

from bautomate.workblock import WorkBlock


class WorkDay:
    """
    Class representing one work day.

    Properties:
        date_day:       Date of the day.
        start_time:     Starting/arrival time on this work day.
        end_time:       Ending/departure time on this work day.
        break_duration: Duration of the break this day.
        mode:           Mode how to set end_time.
        blocks:         List of WorkBlocks.
    """

    def __init__(self, **kwargs):
        self.date_day = kwargs.get("date_day", "1.1.1970")
        self.start_time = kwargs.get("start_time", "08:00")
        self.end_time = kwargs.get("end_time", "16:30")
        self.break_duration = kwargs.get("break_duration", "00:30")
        self.mode = kwargs.get("mode", "normal")
        self.blocks = kwargs.get("blocks", [])

    def __str__(self):
        s = ""
        for k in self.__dict__.keys():
            s += "\n"
            s += f"{k}: {getattr(self, k)}"
        return s

    def __repr__(self):
        s = ""
        for k in self.__dict__.keys():
            s += "\n"
            s += f"{k}: {getattr(self, k)}"
        return s

    @property
    def date_day(self) -> str:
        """Holds the date of a day as a string."""
        return self._date_day

    @date_day.setter
    def date_day(self, s: str) -> None:
        if not isinstance(s, str):
            raise TypeError

        if "." in s:
            a = s.split(".")
        elif "/" in s:
            a = s.split("/")
        elif "-" in s:
            a = s.split("-")
        else:
            raise ValueError

        if len(a[0]) == 4:
            a.reverse()

        # Make sure we get a full four digit year
        if len(a[2]) != 4:
            raise ValueError("Year must be four digits long.")

        self._date_day = "{:02}.{:02}.{}".format(*map(int, a))

    @property
    def start_time(self) -> str:
        """The starting time of work for that day."""
        return self._start_time

    @start_time.setter
    def start_time(self, s: str) -> None:
        if not isinstance(s, str):
            raise TypeError

        if "." in s:
            a = s.split(".")
        elif ":" in s:
            a = s.split(":")

        self._start_time = "{:02}:{:02}".format(*map(int, a))

    @property
    def end_time(self) -> str:
        """The ending time of work for that day."""
        return self._end_time

    @end_time.setter
    def end_time(self, s: str) -> None:
        if not isinstance(s, str):
            raise TypeError

        if "." in s:
            a = s.split(".")
        elif ":" in s:
            a = s.split(":")

        self._end_time = "{:02}:{:02}".format(*map(int, a))

    @property
    def break_duration(self) -> str:
        """The break duration of this day."""
        return self._break_duration

    @break_duration.setter
    def break_duration(self, s: str) -> None:
        if not isinstance(s, str):
            raise TypeError

        if "." in s:
            a = s.split(".")
        elif ":" in s:
            a = s.split(":")

        self._break_duration = "{:02}:{:02}".format(*map(int, a))

    @property
    def mode(self) -> str:
        """
        The mode how to set the end time.

            'normal':       End time is given in data.
            'fill':         The last work block is stretched to fit
                given start, end time, and break duration.
            'calculate':    End time is calculated from sum of hours,
                start time, and break duration.
        """
        return self._mode

    @mode.setter
    def mode(self, s: str) -> None:
        if not isinstance(s, str):
            raise TypeError

        if s.lower() in ["normal", "norm"]:
            self._mode = "normal"
        elif s.lower() in ["fill", "filled"]:
            self._mode = "fill"
            # TODO: Implement this functionality, here or somewhere else?
            raise NotImplementedError
        elif s.lower() in ["calculate", "calc", "calculated"]:
            self._mode = "calculate"
            # TODO: Implement this functionality, here or somewhere else?
            raise NotImplementedError
        else:
            raise ValueError

    @property
    def blocks(self) -> List:
        """List of work blocks/hours of this day."""
        return self._blocks

    @blocks.setter
    def blocks(self, k: List) -> None:
        if not isinstance(k, List):
            raise TypeError

        if not hasattr(self, "_blocks"):
            self._blocks = []

        for e in k:
            self._blocks.append(WorkBlock(**e))
