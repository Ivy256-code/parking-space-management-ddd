import pytest

from src.application.event_handlers.parking_session_created_handler import (
    ParkingSessionCreatedHandler,
)
from src.domain.aggregates.parking_session import ParkingSession
from src.domain.events.event_dispatcher import EventDispatcher
from src.domain.events.parking_session_created import ParkingSessionCreated


class FakeParkingSpace:
    def __init__(self) -> None:
        self.occupy_calls = 0

    def occupy(self) -> None:
        self.occupy_calls += 1


class FakeParkingSpaceRepository:
    def __init__(self, parking_space: FakeParkingSpace | None) -> None:
        self.parking_space = parking_space
        self.looked_up_ids: list[str] = []

    def find(self, parking_space_id: str) -> FakeParkingSpace | None:
        self.looked_up_ids.append(parking_space_id)
        return self.parking_space


def test_dispatching_created_event_occupies_the_retrieved_space() -> None:
    parking_space = FakeParkingSpace()
    repository = FakeParkingSpaceRepository(parking_space)
    dispatcher = EventDispatcher()
    dispatcher.register(
        ParkingSessionCreated,
        ParkingSessionCreatedHandler(repository).handle,
    )
    session = ParkingSession("session-1", "vehicle-1", "space-1")

    dispatcher.dispatch(session.pull_domain_events()[0])

    assert repository.looked_up_ids == ["space-1"]
    assert parking_space.occupy_calls == 1


def test_dispatch_propagates_rejection_from_occupied_space() -> None:
    class OccupiedParkingSpace:
        def occupy(self) -> None:
            raise ValueError("Parking space is already occupied")

    repository = FakeParkingSpaceRepository(OccupiedParkingSpace())
    dispatcher = EventDispatcher()
    session = ParkingSession("session-1", "vehicle-1", "space-1")
    dispatcher.register(ParkingSessionCreated, ParkingSessionCreatedHandler(repository).handle)

    with pytest.raises(ValueError, match="already occupied"):
        dispatcher.dispatch(session.pull_domain_events()[0])


def test_handler_rejects_event_for_missing_space() -> None:
    repository = FakeParkingSpaceRepository(None)
    session = ParkingSession("session-1", "vehicle-1", "space-1")
    dispatcher = EventDispatcher()
    dispatcher.register(ParkingSessionCreated, ParkingSessionCreatedHandler(repository).handle)

    with pytest.raises(LookupError, match="space-1"):
        dispatcher.dispatch(session.pull_domain_events()[0])