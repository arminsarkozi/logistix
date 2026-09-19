# First steps
To get familiar with Logistix, you have to know about the main class definition. When using Logistix to schedule events, you need to create a Scheduler object in your code like below.
```python
from logistix import Scheduler

S = Scheduler(work_time=["08:00", "17:00"])
```

Awesome, you have just created a Scheduler in Logistix. In the arguments, you can specifiy data like:

- `work_time` (in `str` with format `HH:MM`) &mdash; the timeframe where Logistix can schedule events
- `start_time` (in `str` with `utils.consts.DATETIME_FORMAT` format meaning `Y-m-d H:M`) &mdash; the start of time; this is important if you want to schedule events in the past &ndash; then you have to set `start_time` to a date and time that is before `now`. Otherwise, you'll get `logistix.utils.errors.PastTaskError` error.
- `auto` &mdash; to solve scheduling every time you change something like change work time, add an event, ...; it can be helpful if you don't want to call `Scheduler.solve()` each time manually

## Adding events and tasks
We add events and tasks using two methods: `add_event()` and `add_task()`.
For example,
```python
S.add_event("school", 480, "2028-09-06 08:00")
```

In `add_event()`, we specify the `name of the event` (it's useful to give different names to each of the events as we don't use IDs yet), the `duration` and the start time in `utils.consts.DATETIME_FORMAT`.