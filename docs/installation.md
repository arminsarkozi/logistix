# Installation and setup
## Requirements
- Python 3.9 or higher
- pip
## Installation
Install Logistix with the command
```bash
pip install logistix
```

Then import logistix in your code as a library:
```python
from logistix import Scheduler
```

After importing, you have to create a Scheduler class to use Logistix.
```python
from logistix import Scheduler

S = Scheduler(work_time=["08:00", "17:00"])  # Scheduler class
```

Scheduler class has a lot of different parameters and methods, you can read about them in our [First Steps guide](first-steps.md).