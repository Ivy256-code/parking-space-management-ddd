class DomainError(Exception):
    """Base class for all domain rule violations."""


class ParkingSpaceAlreadyOccupiedError(DomainError):
    """Raised when BR3 is violated: the space is already occupied."""

    def __init__(self, space_number: str):
        super().__init__(f"Parking space {space_number} is already occupied.")
        self.space_number = space_number