"""Tests for InMemoryParkingSpaceRepository (BR6 - Lookup Rule)."""

from dataclasses import dataclass

import pytest

from src.infrastructure.repositories.in_memory_parking_space_repository import (
    InMemoryParkingSpaceRepository,
)


@dataclass
class FakeParkingSpace:
    """Minimal stand-in for Ritah's real ParkingSpace aggregate."""

    space_id: str
    status: str = "AVAILABLE"


@pytest.fixture
def repository() -> InMemoryParkingSpaceRepository:
    return InMemoryParkingSpaceRepository()


def test_find_returns_saved_space(repository):
    space = FakeParkingSpace(space_id="space-1")
    repository.save(space)

    assert repository.find_by_id("space-1") is space


def test_find_returns_none_when_space_does_not_exist(repository):
    assert repository.find_by_id("missing") is None


def test_save_replaces_existing_space_with_same_id(repository):
    repository.save(FakeParkingSpace(space_id="space-1", status="AVAILABLE"))
    updated = FakeParkingSpace(space_id="space-1", status="OCCUPIED")
    repository.save(updated)

    assert repository.find_by_id("space-1") is updated


def test_repositories_do_not_share_data():
    first = InMemoryParkingSpaceRepository()
    second = InMemoryParkingSpaceRepository()
    first.save(FakeParkingSpace(space_id="space-1"))

    assert second.find_by_id("space-1") is None