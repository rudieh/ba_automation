class WorkBlock():
    """
    One single work block with hours for one project/activity.

    Properties:
        project_name:   Name of the project
        activity:       Name of the activity inside the project
        duration:       Duration of the activity
    """
    def __init__(self, **kwargs):
        self.project_name = kwargs.get("project_name", '')
        self.activity = kwargs.get("activity", '')
        self.duration = kwargs.get("duration", 1)

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
    def project_name(self):
        """Name of the project."""
        return self._project_name

    @project_name.setter
    def project_name(self, s):
        s = str(s)
        if '\n' in s:
            s = s.replace('\n', '')
        self._project_name = s.strip()

    @property
    def activity(self):
        """Name of the activity inside the project."""
        return self._activity

    @activity.setter
    def activity(self, s):
        s = str(s)
        if '\n' in s:
            s = s.replace('\n', '')
        self._activity = s.strip()

    @property
    def duration(self):
        """Duration given in minutes, in format '8:00', or in hours as float value."""
        return self._duration

    @duration.setter
    def duration(self, n):
        if isinstance(n, float):
            n = self._calculate_minute(n)
        elif isinstance(n, str) and (':' in n or '.' in n):
            n = self._convert_to_minute(n)

        n = int(n)
        if n <= 0 or n > 60*10:
            raise ValueError
        self._duration = n

    def _convert_to_minute(self, n: str) -> int:
        if ':' in n:
            h, m = n.split(':')
        elif '.' in n:
            h, m = n.split('.')
        h = int(h)
        m = int(m)
        return h*60 + m

    def _calculate_minute(self, n: float) -> int:
        return int(n * 60)