import pytest

from src.domain.aggregates.parking_space import ParkingSpace, ParkingSpaceStatus
from src.domain.errors import ParkingSpaceAlreadyOccupiedError
from src.domain.value_objects.parking_space_number import ParkingSpaceNumber


def make_space(space_id="S1", number="PS-001"):
    return ParkingSpace(space_id, ParkingSpaceNumber(number))


# ---------- BR2: state change (AVAILABLE -> OCCUPIED) ----------

def test_new_parking_space_is_available():
    space = make_space()
    assert space.status == ParkingSpaceStatus.AVAILABLE


def test_occupy_changes_available_space_to_occupied():  # T2
    space = make_space()
    space.occupy()
    assert space.status == ParkingSpaceStatus.OCCUPIED


# ---------- BR3: invariant (occupied space cannot be occupied again) ----------

def test_occupying_an_occupied_space_is_rejected():  # T3 (rejection test)
    space = make_space()
    space.occupy()
    with pytest.raises(ParkingSpaceAlreadyOccupiedError):
        space.occupy()


def test_rejected_occupy_leaves_state_unchanged():
    space = make_space()
    space.occupy()
    with pytest.raises(ParkingSpaceAlreadyOccupiedError):
        space.occupy()
    assert space.status == ParkingSpaceStatus.OCCUPIED


# ---------- Entity identity ----------

def test_spaces_with_same_id_are_equal():
    assert make_space("S1", "PS-001") == make_space("S1", "PS-001")


def test_spaces_with_different_ids_are_not_equal_even_with_same_number():
    assert make_space("S1", "PS-001") != make_space("S2", "PS-001")


def test_empty_space_id_is_rejected():
    with pytest.raises(ValueError):
        ParkingSpace("", ParkingSpaceNumber("PS-001"))