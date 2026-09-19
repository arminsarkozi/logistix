from ortools.sat.python import cp_model
from datetime import datetime
from .utils import time, errors, consts

# Constants
FOREVER = (
    10000  # For repeat events: 10.000 days (approx. 27,4 y) or weeks (approx. 191,7 y)
)


class Scheduler:
    def __init__(self, work_time=None, auto=False, **kwargs):
        self.work_time = work_time if work_time else ["00:00", "23:59"]
        self.model = cp_model.CpModel()

        self.task_intervals = []
        self.event_intervals = []
        self.all_intervals = []

        self.start_values = {}
        self.presence_vars = {}

        self.time = time.TimeManager(start_time=kwargs.get("start_time"))

        self.auto = auto  # Automatic solving after each modification
        self.set_work_time(work_time)

    def auto_solve(self):
        if self.auto:
            self.solve()

    def set_work_time(self, work_time):
        self.work_time = work_time if work_time else ["00:00", "23:59"]
        # Parse work_time into minute offsets from midnight (e.g., "08:20" -> 8 * 60 + 20 = 500)
        t_start = datetime.strptime(self.work_time[0], "%H:%M")
        t_end = datetime.strptime(self.work_time[1], "%H:%M")
        self.work_start = t_start.hour * 60 + t_start.minute
        self.work_end = t_end.hour * 60 + t_end.minute

        self.auto_solve()

    def add_event(self, event_name, duration, start_time, repeat=None):
        """Fixed events can overlap each other, but block out task time."""
        start = self.time.time_to_minutes(start_time)

        event = self.model.new_fixed_size_interval_var(start, duration, event_name)
        self.event_intervals.append(event)
        self.all_intervals.append(event)

        if repeat == "yearly" or repeat == "annually":
            year = 365 * 24 * 60
            for i in range(1, FOREVER + 1):
                event = self.model.new_fixed_size_interval_var(
                    start + year, duration, f"{event_name}_{i}"
                )
                self.event_intervals.append(event)
                self.all_intervals.append(event)
        elif repeat == "weekly":
            week = 168 * 60
            for i in range(1, FOREVER + 1):
                event = self.model.new_fixed_size_interval_var(
                    start + week, duration, f"{event_name}_{i}"
                )
                self.event_intervals.append(event)
                self.all_intervals.append(event)
        elif repeat == "biweekly":
            week = 168 * 60 * 2
            for i in range(1, FOREVER + 1):
                event = self.model.new_fixed_size_interval_var(
                    start + week, duration, f"{event_name}_{i}"
                )
                self.event_intervals.append(event)
                self.all_intervals.append(event)
        elif repeat == "daily":
            day = 24 * 60
            for i in range(1, FOREVER + 1):
                event = self.model.new_fixed_size_interval_var(
                    start + day, duration, f"{event_name}_{i}"
                )
                self.event_intervals.append(event)
                self.all_intervals.append(event)

        self.auto_solve()

    def add_task(self, task_name, duration, deadline):
        """Add a task to schedule by the AI. Tasks restricted strictly to daily work_time hours."""

        if datetime.strptime(deadline, consts.DATETIME_FORMAT) < datetime.now().replace(
            second=0, microsecond=0
        ):
            raise errors.PastTaskError()

        # Define the earliest and the latest start of the current task
        self.start_values[task_name] = self.model.new_int_var(
            self.time.now(),  # Earliest start can be now
            self.time.time_to_minutes(deadline)
            - duration,  # The latest start time can be added so that the end of the task is before or exactly at deadline
            f"{task_name}_start",  # Name of the task start time int variable
        )

        # Define start and end variables that are going to be scheduled
        start_var = self.start_values[task_name]
        end_var = self.model.new_int_var(
            self.time.now(),  # We can end this task as early as now
            self.time.time_to_minutes(
                deadline
            ),  # The end time of task can be before or on the deadline
            f"{task_name}_end",  # Name of the task end time int variable
        )
        # The end of the event is `duration` mins after the start
        self.model.add(end_var == start_var + duration)

        # In some cases, we cannot schedule an event
        present = self.model.new_bool_var(
            f"{task_name}_present"
        )  # Whether we schedule it or rejected
        self.presence_vars[task_name] = present  # Save `presence` book variable
        task = self.model.new_optional_fixed_size_interval_var(
            start_var, duration, present, task_name
        )  # The task variable
        # Appending task to the appropriate interval lists
        self.task_intervals.append(task)
        self.all_intervals.append(task)

        # Daily Work-Time Constraints (Modulo 1440 minutes in a day)
        # Calculate start and end offsets from local midnight (since self.start_time)
        midnight_offset = (self.time.start_time.hour * 60) + self.time.start_time.minute

        # Calculate total day index and minute-of-day offsets directly without modulo wrapping tricks
        start_abs = start_var + midnight_offset
        end_abs = end_var + midnight_offset

        # Require that the task starts and ends on the SAME day
        day_index = self.model.new_int_var(0, 10000, f"{task_name}_day_index")
        self.model.add_division_equality(day_index, start_abs, 1440)

        start_day = self.model.new_int_var(0, 1439, f"{task_name}_start_day")
        end_day = self.model.new_int_var(0, 1439, f"{task_name}_end_day")

        # Enforce start and end times within day_index
        self.model.add(start_abs == day_index * 1440 + start_day).only_enforce_if(
            present
        )
        self.model.add(end_abs == day_index * 1440 + end_day).only_enforce_if(present)

        # Strict work hours check
        self.model.add(start_day >= self.work_start).only_enforce_if(present)
        self.model.add(end_day <= self.work_end).only_enforce_if(present)
        self.model.add(end_day > start_day).only_enforce_if(present)

        self.auto_solve()

        return self.start_values[task_name]

    def solve(self):
        """Solve constraint problem, i.e. schedule tasks."""
        self.model.add_no_overlap(self.task_intervals)
        for task_interval in self.task_intervals:
            for event_interval in self.event_intervals:
                self.model.add_no_overlap([task_interval, event_interval])
        self.model.maximize(sum(self.presence_vars.values()))

        solver = cp_model.CpSolver()
        status = solver.solve(self.model)

        solution = dict()
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            for key in self.start_values.keys():
                is_scheduled = solver.value(self.presence_vars[key])
                if is_scheduled:
                    start_minute = solver.value(self.start_values[key])
                    solution[key] = self.time.minutes_to_time(start_minute)
                else:
                    solution[key] = "NOT OK (cannot fit before deadline)"
        else:
            raise Exception("No overall solution exists")
        return solution

    def print_solution(self):
        """Print solution start times to console (command line) in text."""
        solution = self.solve()
        for key, start in solution.items():
            print(f"Task '{key}': {start}")
