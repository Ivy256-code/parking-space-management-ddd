"""Unit tests for AssignParkingSpaceService (BR6 - Lookup Rule)."""

import pytest

from src.application.dto.assign_parking_space_dto import AssignParkingSpaceRequest
from src.application.services.assign_parking_space_service import (
    AssignParkingSpaceService,
)
from src.domain.aggregates.parking_space import ParkingSpace
from src.domain.value_objects.parking_space_number import ParkingSpaceNumber
from src.infrastructure.repositories.in_memory_parking_space_repository import (
    InMemoryParkingSpaceRepository,
)


class DispatcherSpy:
    """Records the events it receives instead of handling them."""

    def __init__(self) -> None:
        self.events = []

    def dispatch(self, event) -> None:
        self.events.append(event)


@pytest.fixture
def repository() -> InMemoryParkingSpaceRepository:
    repo = InMemoryParkingSpaceRepository()
    repo.save(ParkingSpace("PS-001", ParkingSpaceNumber("PS-001")))
    return repo


@pytest.fixture
def dispatcher() -> DispatcherSpy:
    return DispatcherSpy()


@pytest.fixture
def service(repository, dispatcher) -> AssignParkingSpaceService:
    return AssignParkingSpaceService(repository, dispatcher, lambda: "session-1")


def test_existing_space_is_assigned_successfully(service):
    result = service.assign(AssignParkingSpaceRequest("v1", "PS-001"))

    assert result.success is True
    assert result.session_id == "session-1"


def test_created_event_carries_the_requested_vehicle_and_space(service, dispatcher):
    service.assign(AssignParkingSpaceRequest("v1", "PS-001"))

    assert len(dispatcher.events) == 1
    assert dispatcher.events[0].vehicle_id == "v1"
    assert dispatcher.events[0].parking_space_id == "PS-001"


def test_missing_space_is_rejected(service):
    result = service.assign(AssignParkingSpaceRequest("v1", "PS-999"))

    assert result.success is False
    assert "PS-999" in result.message
    assert result.session_id is None


def test_no_event_is_dispatched_when_space_is_missing(service, dispatcher):
    service.assign(AssignParkingSpaceRequest("v1", "PS-999"))

    assert dispatcher.events == []