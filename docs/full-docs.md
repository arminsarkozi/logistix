## Installation
Look at [our installation guide](installation.md).

## class Scheduler(work_time = None, **kwargs)

Main scheduler class responsible for creating and solving
constraint-based schedules.

### Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| **work_time** | `tuple[str, str]` | The daily time range in which tasks may be scheduled. Default value is `None`. If given no value (or None), it assumes all-day activity is available (from 0:00 to 23:59). |

### Consts
`utils.consts.DATETIME_FORMAT` = `Y-m-d H:M` str

### Methods

#### set_work_time(work_time)

Set work time a new value.

**Parameters**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| **work_time** | `tuple[str, str]` | The daily time range in which tasks may be scheduled. Default value is `None`. If given no value (or None), it assumes all-day activity is available (from 0:00 to 23:59). |
| **auto** | `boolean` | Automatic solving after each important modification like changing the work time or adding a task. Default is `False`. Note that it'll extend the compiling time a bit. |
| **start_time** | `str` in `DATETIME_FORMAT` format | Specify a custom start time than the date of the creation. |

**Returns**

Nothing.

---

#### add_event(event_name, duration, start_time, repeat=None)

Add a fixed event to the schedule. When scheduling, it is _fixed_ meaning the AI does not move it.

**Parameters**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| **event_name** | `str` | Name of the event to add. |
| **duration** | `int` | Duration of the event. |
| **repeat** | `str | None` | Repeating event. Default is `None` meaning not repeating, but it can be `daily`, `weekly`, `biweekly`, `yearly` or `annually`. |

---

#### add_task(self, task_name, duration, deadline)

Add a dynamic (schedulable) event to the pool - the AI will schedule it.

**Parameters**

| Parameter | Type | Description |
| :--- | :--- | :--- |
| **task_name** | `str` | Name of the task to add. |
| **duration** | `int` | Duration of the task. |
| **deadline** | `str` in `DATETIME_FORMAT` format | Deadline of the task to take. |

---

#### solve()

Solve the scheduling problem.

**Returns**

`Schedule`
: The resulting schedule.

**Raises**

`Exception("No overall solution exists")`
: If no feasible schedule exists.

---

#### print_solution()

Prints solution to command line in text format using `Schedule.solve()`

**Raises**

-
`Exception("No overall solution exists")` if `Schedule.solve()` does that