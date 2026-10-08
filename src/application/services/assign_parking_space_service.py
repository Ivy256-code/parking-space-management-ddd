"""Application service for the 'Assign Parking Space' use case."""

from typing import Callable

from src.application.dto.assign_parking_space_dto import (
    AssignParkingSpaceRequest,
    AssignParkingSpaceResult,
)
from src.domain.repositories.parking_space_repository import ParkingSpaceRepository

# A function that takes (vehicle_id, space_id) and returns the new session's ID.
# Mark's ParkingSession work will be plugged in here later.
SessionCreator = Callable[[str, str], str]


class AssignParkingSpaceService:
    """Coordinates the use case. It contains no business rules of its own."""

    def __init__(
        self,
        repository: ParkingSpaceRepository,
        create_session: SessionCreator,
    ) -> None:
        self._repository = repository
        self._create_session = create_session

    def assign(self, request: AssignParkingSpaceRequest) -> AssignParkingSpaceResult:
        parking_space = self._repository.find_by_id(request.space_id)

        if parking_space is None:  # BR6: no space found, so reject
            return AssignParkingSpaceResult.rejected(
                f"Parking space '{request.space_id}' not found."
            )

        session_id = self._create_session(request.vehicle_id, request.space_id)
        return AssignParkingSpaceResult.succeeded(session_id)