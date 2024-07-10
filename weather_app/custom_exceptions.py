"""Module for custom exceptions."""
class DataError(Exception):
    """an exception to store status code and error message"""
    def __init__(self, status, message):
        super().__init__(status, message)
        self.status = status
        self.message = message

    def __str__(self):
        return f'Error {self.status}, \"{self.message}\"! couldn\'t retrieve api data'
