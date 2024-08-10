from datetime import datetime

class UtilitiesService:
    """Service class for utility functions."""

    def get_current_year(self) -> int:
        """Returns the current year."""
        return datetime.now().year
