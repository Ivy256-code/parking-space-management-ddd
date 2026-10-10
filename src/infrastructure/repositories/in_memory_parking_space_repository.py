"""In-memory implementation of ParkingSpaceRepository."""

from typing import Dict, Optional, TYPE_CHECKING

from src.domain.repositories.parking_space_repository import ParkingSpaceRepository

if TYPE_CHECKING:
    # Used only for type hints. Adjust this path to match Ritah's file.
    from src.domain.aggregates.parking_space import ParkingSpace


class InMemoryParkingSpaceRepository(ParkingSpaceRepository):
    """Keeps parking spaces in a dictionary. No database needed."""

    def __init__(self) -> None:
        self._spaces: Dict[str, "ParkingSpace"] = {}

    def find_by_id(self, space_id: str) -> Optional["ParkingSpace"]:
        return self._spaces.get(space_id)
    def find(self, parking_space_id: str) -> Optional["ParkingSpace"]:
        """Name used by Mark's event handler. Same as find_by_id."""
        return self.find_by_id(parking_space_id)

    def save(self, parking_space: "ParkingSpace") -> None:
        self._spaces[parking_space.space_id] = parking_space