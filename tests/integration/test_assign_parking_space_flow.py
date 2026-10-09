"""Integration tests T7 (success) and T8 (failure) for Assign Parking Space."""

import pytest

from src.application.dto.assign_parking_space_dto import AssignParkingSpaceRequest
from src.application.event_handlers.parking_session_created_handler import (
    ParkingSessionCreatedHandler,
)
from src.application.services.assign_parking_space_service import (
    AssignParkingSpaceService,
)
from src.domain.aggregates.parking_space import ParkingSpace, ParkingSpaceStatus
from src.domain.events.event_dispatcher import EventDispatcher
from src.domain.events.parking_session_created import ParkingSessionCreated
from src.domain.value_objects.parking_space_number import ParkingSpaceNumber
from src.infrastructure.repositories.in_memory_parking_space_repository import (
    InMemoryParkingSpaceRepository,
)


@pytest.fixture
def system():
    repository = InMemoryParkingSpaceRepository()
    repository.save(ParkingSpace("PS-001", ParkingSpaceNumber("PS-001")))

    dispatcher = EventDispatcher()
    dispatcher.register(
        ParkingSessionCreated, ParkingSessionCreatedHandler(repository).handle
    )
    service = AssignParkingSpaceService(repository, dispatcher)
    return service, repository


def test_t7_available_space_is_assigned_and_becomes_occupied(system):
    service, repository = system
    assert repository.find_by_id("PS-001").status == ParkingSpaceStatus.AVAILABLE

    result = service.assign(AssignParkingSpaceRequest("v1", "PS-001"))

    assert result.success is True
    assert result.session_id is not None
    assert repository.find_by_id("PS-001").status == ParkingSpaceStatus.OCCUPIED


def test_t8_occupied_space_cannot_be_assigned_again(system):
    service, repository = system

    service.assign(AssignParkingSpaceRequest("v1", "PS-001"))

    result = service.assign(AssignParkingSpaceRequest("v2", "PS-001"))

    assert result.success is False
    assert "already occupied" in result.message
    assert result.session_id is None
    assert repository.find_by_id("PS-001").status == ParkingSpaceStatus.OCCUPIED