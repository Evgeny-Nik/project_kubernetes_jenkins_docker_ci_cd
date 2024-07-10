"""Module for custom classes."""
class ErrorDict: # pylint: disable=too-few-public-methods
    """class used to store the appropriate error code"""
    str_dict = {
        400: 'invalid location',
        401: 'invalid API key',
        429: 'reached request limit',
        500: 'API side server error, try again later'
    }
