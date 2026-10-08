from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ParkingSessionCreated:
    session_id: str
    parking_space_id: str
    vehicle_id: str
    occurred_at: datetime