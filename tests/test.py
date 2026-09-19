from logistix import Scheduler

S = Scheduler(work_time=["08:00", "17:00"])
# S.add_event("school", 480, "2028-09-06 08:00")
# S.add_event("doctor", 60, "2028-09-06 16:00")
# S.add_event("meeting", 60, "2028-09-06 16:00")
# S.add_event("repeat event", 60, "2026-08-28 08:00", repeat="weekly")

# # Tasks
# S.add_task("Harvard", 120, "2028-09-04 20:00")
# S.add_task("CS50 AI", 180, "2028-09-07 20:00")
# S.add_task("programming", 90, "2028-09-05 18:00")
# S.add_task("math", 120, "2028-09-04 12:00")

S.add_event("verseny", 300, "2026-09-12 15:50")
S.add_task("elvégezni a házi feladatokat", 60, "2026-09-14 08:00")

S.print_solution()
