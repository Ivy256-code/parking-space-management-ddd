from enum import Enum


class VehicleCategory(Enum):
    """The kinds of vehicle that can park. Each has its own hourly rate."""

    MOTORCYCLE = "MOTORCYCLE"
    CAR = "CAR"
    TRUCK = "TRUCK"