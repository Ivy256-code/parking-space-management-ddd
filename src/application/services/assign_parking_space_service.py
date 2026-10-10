"""Application service for the 'Assign Parking Space' use case."""

import uuid
from typing import Callable

from src.application.dto.assign_parking_space_dto import (
    AssignParkingSpaceRequest,
    AssignParkingSpaceResult,
)
from src.domain.aggregates.parking_session import ParkingSession
from src.domain.errors import DomainError
from src.domain.events.event_dispatcher import EventDispatcher
from src.domain.repositories.parking_space_repository import ParkingSpaceRepository


def _new_session_id() -> str:
    return str(uuid.uuid4())


class AssignParkingSpaceService:
    """Coordinates the use case. Business rules stay in the domain."""

    def __init__(
        self,
        repository: ParkingSpaceRepository,
        dispatcher: EventDispatcher,
        generate_session_id: Callable[[], str] = _new_session_id,
    ) -> None:
        self._repository = repository
        self._dispatcher = dispatcher
        self._generate_session_id = generate_session_id

    def assign(self, request: AssignParkingSpaceRequest) -> AssignParkingSpaceResult:
        parking_space = self._repository.find_by_id(request.space_id)

        if parking_space is None:  # BR6: no space found, so reject
            return AssignParkingSpaceResult.rejected(
                f"Parking space '{request.space_id}' not found."
            )

        session = ParkingSession(
            self._generate_session_id(), request.vehicle_id, request.space_id
        )

        try:
            # Mark's handler occupies the space when the event is dispatched.
            for event in session.pull_domain_events():
                self._dispatcher.dispatch(event)
        except DomainError as error:  # BR3: space already occupied
            return AssignParkingSpaceResult.rejected(str(error))

        self._repository.save(parking_space)
        return AssignParkingSpaceResult.succeeded(session.session_id)