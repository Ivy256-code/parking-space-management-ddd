import math
from datetime import timedelta
from typing import Mapping

from src.domain.value_objects.vehicle_category import VehicleCategory

SECONDS_PER_HOUR = 3600

# Hourly rates in UGX, kept in one place so they are easy to change.
DEFAULT_HOURLY_RATES: dict[VehicleCategory, int] = {
    VehicleCategory.MOTORCYCLE: 1000,
    VehicleCategory.CAR: 2000,
    VehicleCategory.TRUCK: 5000,
}


class ParkingFeeService:
    """Domain service for BR4.

    Fee = billable hours x hourly rate of the vehicle category.
    The service keeps no state; it only performs the calculation.
    """

    def __init__(
        self, hourly_rates: Mapping[VehicleCategory, int] | None = None
    ) -> None:
        rates = DEFAULT_HOURLY_RATES if hourly_rates is None else hourly_rates
        self._hourly_rates = dict(rates)

    def calculate_fee(self, category: VehicleCategory, duration: timedelta) -> int:
        """Return the parking fee in whole UGX.

        Partial hours are charged as a full hour.

        Raises:
            ValueError: if the category is invalid, has no rate,
                or the duration is zero or negative.
        """
        if not isinstance(category, VehicleCategory):
            raise ValueError("category must be a VehicleCategory")
        if duration <= timedelta(0):
            raise ValueError("duration must be greater than zero")
        if category not in self._hourly_rates:
            raise ValueError(f"no rate defined for {category.name}")

        return self._billable_hours(duration) * self._hourly_rates[category]

    @staticmethod
    def _billable_hours(duration: timedelta) -> int:
        """Round the duration up to whole hours."""
        return math.ceil(duration.total_seconds() / SECONDS_PER_HOUR)