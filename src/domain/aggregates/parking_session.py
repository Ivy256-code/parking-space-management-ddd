from datetime import datetime, timezone
from enum import Enum

from src.domain.events.parking_session_created import ParkingSessionCreated


class SessionStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ENDED = "ENDED"


class ParkingSession:
    def __init__(
        self,
        session_id: str,
        vehicle_id: str,
        parking_space_id: str,
        start_time: datetime | None = None,
    ) -> None:
        self.session_id = session_id
        self.vehicle_id = vehicle_id
        self.parking_space_id = parking_space_id
        self.start_time = start_time or datetime.now(timezone.utc)
        self.status = SessionStatus.ACTIVE
        self._domain_events = [
            ParkingSessionCreated(
                session_id=session_id,
                parking_space_id=parking_space_id,
                vehicle_id=vehicle_id,
                occurred_at=self.start_time,
            )
        ]

    @property
    def domain_events(self) -> tuple[ParkingSessionCreated, ...]:
        return tuple(self._domain_events)

    def pull_domain_events(self) -> tuple[ParkingSessionCreated, ...]:
        events = self.domain_events
        self._domain_events.clear()
        return events