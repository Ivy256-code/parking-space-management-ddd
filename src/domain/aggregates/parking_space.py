from enum import Enum

from src.domain.errors import ParkingSpaceAlreadyOccupiedError
from src.domain.value_objects.parking_space_number import ParkingSpaceNumber


class ParkingSpaceStatus(Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"


class ParkingSpace:
    """Entity and Aggregate Root.

    BR2: a space can move from AVAILABLE to OCCUPIED.
    BR3: an OCCUPIED space cannot be occupied again.
    """

    def __init__(self, space_id: str, number: ParkingSpaceNumber):
        if not space_id:
            raise ValueError("space_id must not be empty")
        self._space_id = space_id
        self._number = number
        self._status = ParkingSpaceStatus.AVAILABLE

    @property
    def space_id(self) -> str:
        return self._space_id

    @property
    def number(self) -> ParkingSpaceNumber:
        return self._number

    @property
    def status(self) -> ParkingSpaceStatus:
        return self._status

    def occupy(self) -> None:
        """BR2: AVAILABLE -> OCCUPIED.
        BR3: reject if already OCCUPIED; the state stays unchanged."""
        if self._status == ParkingSpaceStatus.OCCUPIED:
            raise ParkingSpaceAlreadyOccupiedError(self._number.value)
        self._status = ParkingSpaceStatus.OCCUPIED

    def __eq__(self, other):
        return isinstance(other, ParkingSpace) and self._space_id == other._space_id

    def __hash__(self):
        return hash(self._space_id)