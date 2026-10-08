"""Repository interface for ParkingSpace (BR6 - Lookup Rule)."""

from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    # Used only for type hints. Adjust this path to match Ritah's file.
    from src.domain.aggregates.parking_space import ParkingSpace


class ParkingSpaceRepository(ABC):
    """Contract for finding and storing ParkingSpace aggregates."""

    @abstractmethod
    def find_by_id(self, space_id: str) -> Optional["ParkingSpace"]:
        """Return the parking space, or None if it does not exist."""

    @abstractmethod
    def save(self, parking_space: "ParkingSpace") -> None:
        """Store a new parking space or update an existing one."""