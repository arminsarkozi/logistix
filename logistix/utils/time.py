from datetime import datetime, timedelta
from . import consts


class TimeManager:
    def __init__(self, start_time):
        self.start_time = datetime.now().replace(
            second=0, microsecond=0
        )  # Creation time of the scheduler
        if start_time:
            self.start_time = datetime.strptime(start_time, consts.DATETIME_FORMAT)

    def time_to_minutes(self, time: str):
        t = datetime.strptime(
            time, consts.DATETIME_FORMAT
        )  # Convert time to `datetime` format
        return int((t - self.start_time).total_seconds() // 60)

    def minutes_to_time(self, mins):
        return self.start_time + timedelta(minutes=mins)

    def now(self):
        return int((datetime.now() - self.start_time).total_seconds() // 60)
