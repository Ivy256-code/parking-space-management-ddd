
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ParkingSpaceNumber:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValueError(
                "Parking space number must be a string"
            )

        if not re.fullmatch(r"PS-\d{3}", self.value):
            raise ValueError(
                "Parking space number must follow "
                "the format PS-001"
            )

    def __str__(self):
        return self.value