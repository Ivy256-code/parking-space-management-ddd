"""DTOs for the 'Assign Parking Space' use case."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AssignParkingSpaceRequest:
    """Data needed to ask for a parking space."""

    vehicle_id: str
    space_id: str


@dataclass(frozen=True)
class AssignParkingSpaceResult:
    """Outcome of the request: either success or a rejection with a reason."""

    success: bool
    message: str
    session_id: Optional[str] = None

    @classmethod
    def succeeded(cls, session_id: str) -> "AssignParkingSpaceResult":
        return cls(success=True, message="Parking space assigned.", session_id=session_id)

    @classmethod
    def rejected(cls, reason: str) -> "AssignParkingSpaceResult":
        return cls(success=False, message=reason)