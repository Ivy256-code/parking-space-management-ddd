from datetime import datetime, timezone

from src.domain.aggregates.parking_session import ParkingSession, SessionStatus
from src.domain.events.parking_session_created import ParkingSessionCreated


def test_creating_session_records_one_created_event_with_session_data() -> None:
    start_time = datetime(2026, 10, 8, 12, 30, tzinfo=timezone.utc)

    session = ParkingSession(
        session_id="session-1",
        vehicle_id="vehicle-1",
        parking_space_id="space-1",
        start_time=start_time,
    )

    events = session.domain_events
    assert session.status is SessionStatus.ACTIVE
    assert len(events) == 1
    assert events[0] == ParkingSessionCreated(
        session_id="session-1",
        parking_space_id="space-1",
        vehicle_id="vehicle-1",
        occurred_at=start_time,
    )


def test_pulling_domain_events_clears_aggregate_event_queue() -> None:
    session = ParkingSession("session-1", "vehicle-1", "space-1")

    pulled_events = session.pull_domain_events()

    assert len(pulled_events) == 1
    assert session.domain_events == ()