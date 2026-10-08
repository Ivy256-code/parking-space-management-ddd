"""Tests for AssignParkingSpaceService (BR6 - Lookup Rule)."""

from dataclasses import dataclass

import pytest

from src.application.dto.assign_parking_space_dto import AssignParkingSpaceRequest
from src.application.services.assign_parking_space_service import (
    AssignParkingSpaceService,
)
from src.infrastructure.repositories.in_memory_parking_space_repository import (
    InMemoryParkingSpaceRepository,
)


@dataclass
class FakeParkingSpace:
    """Minimal stand-in for Ritah's real ParkingSpace aggregate."""

    space_id: str
    status: str = "AVAILABLE"


class SessionCreatorSpy:
    """Stand-in for Mark's session creation. Records how it was called."""

    def __init__(self) -> None:
        self.calls = []

    def __call__(self, vehicle_id: str, space_id: str) -> str:
        self.calls.append((vehicle_id, space_id))
        return "session-1"


@pytest.fixture
def repository() -> InMemoryParkingSpaceRepository:
    repo = InMemoryParkingSpaceRepository()
    repo.save(FakeParkingSpace(space_id="PS-001"))
    return repo


@pytest.fixture
def session_creator() -> SessionCreatorSpy:
    return SessionCreatorSpy()


@pytest.fixture
def service(repository, session_creator) -> AssignParkingSpaceService:
    return AssignParkingSpaceService(repository, session_creator)


def test_existing_space_is_assigned_successfully(service):
    result = service.assign(AssignParkingSpaceRequest("v1", "PS-001"))

    assert result.success is True
    assert result.session_id == "session-1"


def test_session_is_created_with_the_requested_vehicle_and_space(
    service, session_creator
):
    service.assign(AssignParkingSpaceRequest("v1", "PS-001"))

    assert session_creator.calls == [("v1", "PS-001")]


def test_missing_space_is_rejected(service):
    result = service.assign(AssignParkingSpaceRequest("v1", "PS-999"))

    assert result.success is False
    assert "PS-999" in result.message
    assert result.session_id is None


def test_no_session_is_created_when_space_is_missing(service, session_creator):
    service.assign(AssignParkingSpaceRequest("v1", "PS-999"))

    assert session_creator.calls == []