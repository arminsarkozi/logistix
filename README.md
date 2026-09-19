# Logistix
**Logistix** is a **Python package** based on Google's `OR-Tools` (CP-SAT) that helps scheduling events and tasks with strict rules like `work_time` period.

We define **two main types of activities**:
- **events**: A fixed activity that we do not schedule in our solver. We use them to reserve time slots for tasks.
- **tasks**: A task is an activity needs scheduling

## How do we do that?
We use CP-SAT of Google OR-Tools because of their efficiency, speed and compatibility with Python.

## How to Contribute
Feel free to contribute to our project! Your contribution counts for us. You can do this in multiple ways.
1. You find a problem in our package when using it or suggest a new feature you think is important? Just open a new issue in our GitHub, write down your problem or recommendation and wait for the maintainers or someone else who'll implement the change by making a pull request.
2. Are you interested in writing code for the package, to contribute in the development of our codebase? Then a) you can write an issue then immediately try to implement that and make a pull request. Or, b) you can just implement without an issue.
3. You can also make changes in the docs with pull requests.

`Important!` It is not obvious we accept the issue and the pull request. This may be against our policies and product development direction. It is recommended to read our CONTRIBUTION.md file to know about the main things. To get familiar with the code, we recommend our DOCS folder containing `full-docs.md` (the full documentation) and other guides on our website.

Tip:
- To launch docs page locally, you should run `zensical serve`


# Future Plans
- Maybe we extend our package to other languages like JavaScript (`npm`) or Java based on the popularity and need.