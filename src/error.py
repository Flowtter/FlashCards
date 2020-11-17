class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class VersionAhead(Error):
    """When the local version is ahead of the online version"""

    def __init__(self, message):
        self.message = message


class TimeOut(Error):
    """Download resulted with a time out"""

    def __init__(self, message):
        self.message = message
