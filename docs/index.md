# Welcome to Logistix

**Logistix** is a Python package designed to schedule activities (events and tasks) in a timeline for the best fit.

Logistix uses the so-called `CP-SAT` implemented by Google. Google OR-Tools (the project name of CP-SAT) is an extremely efficient solver for mathematical problems in the topic of [Constraint Programming](https://en.wikipedia.org/wiki/Constraint_programming). However, using CP-SAT is quite complicated if you would like to schedule tasks with constraints like:

- you only do tasks **in your work time**
- you cannot schedule your tasks when you have a fixed event (e.g. meeting, school)
- if you cannot schedule your task today, schedule it tomorrow, if not tomorrow, the day after ...
- you have to do your tasks before **deadline**
- you know what's the **duration** of completing the task
- ...

Logistix helps in that! By writing simple, short code lines, it does the hard part of time scheduling. Are you interested? Let's dive in the basics of the package.

## Available guides
- [Installation](installation.md)
- [First steps](first-steps.md)

## Recent posts
[View all posts →](blog/index.md)