class ObdTrackerError(Exception):
    """Base exception for obdtracker."""
    pass

class ObdTrackerAuthError(ObdTrackerError):
    """Exception raised for authentication errors."""
    pass

class ObdTrackerConnectionError(ObdTrackerError):
    """Exception raised for connection errors."""
    pass

class ObdTrackerParseError(ObdTrackerError):
    """Exception raised when response parsing fails."""
    pass
