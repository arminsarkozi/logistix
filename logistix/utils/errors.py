class PastTaskError(Exception):
    def __init__(self, message="Given time of task is in the past"):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"PastTaskError: {self.message}"
