from typing import Protocol

from src.domain.events.parking_session_created import ParkingSessionCreated


class OccupiableParkingSpace(Protocol):
    def occupy(self) -> None: ...


class ParkingSpaceRepository(Protocol):
    def find(self, parking_space_id: str) -> OccupiableParkingSpace | None: ...


class ParkingSessionCreatedHandler:
    def __init__(self, parking_space_repository: ParkingSpaceRepository) -> None:
        self._parking_space_repository = parking_space_repository

    def handle(self, event: ParkingSessionCreated) -> None:
        parking_space = self._parking_space_repository.find(event.parking_space_id)
        if parking_space is None:
            raise LookupError(f"Parking space not found: {event.parking_space_id}")
        parking_space.occupy()