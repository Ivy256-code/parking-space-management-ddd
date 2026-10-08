from datetime import timedelta

import pytest

from src.domain.services.parking_fee_service import ParkingFeeService
from src.domain.value_objects.vehicle_category import VehicleCategory

TEST_RATES = {
    VehicleCategory.MOTORCYCLE: 1000,
    VehicleCategory.CAR: 2000,
    VehicleCategory.TRUCK: 5000,
}


@pytest.fixture
def service() -> ParkingFeeService:
    # Fixed rates, so tests never break if the real prices change.
    return ParkingFeeService(hourly_rates=TEST_RATES)


@pytest.mark.parametrize(
    "category, duration, expected_fee",
    [
        (VehicleCategory.CAR, timedelta(hours=3), 6000),
        (VehicleCategory.CAR, timedelta(hours=1), 2000),
        (VehicleCategory.CAR, timedelta(minutes=61), 4000),
        (VehicleCategory.MOTORCYCLE, timedelta(minutes=1), 1000),
        (VehicleCategory.MOTORCYCLE, timedelta(hours=2), 2000),
        (VehicleCategory.TRUCK, timedelta(hours=2), 10000),
    ],
)
def test_fee_is_calculated_from_rate_and_rounded_up_hours(
    service, category, duration, expected_fee
):
    assert service.calculate_fee(category, duration) == expected_fee


@pytest.mark.parametrize("duration", [timedelta(0), timedelta(hours=-1)])
def test_zero_or_negative_duration_is_rejected(service, duration):
    with pytest.raises(ValueError, match="greater than zero"):
        service.calculate_fee(VehicleCategory.CAR, duration)


def test_invalid_category_is_rejected(service):
    with pytest.raises(ValueError, match="VehicleCategory"):
        service.calculate_fee("CAR", timedelta(hours=1))


def test_category_without_a_rate_is_rejected():
    service = ParkingFeeService(hourly_rates={VehicleCategory.CAR: 2000})

    with pytest.raises(ValueError, match="no rate defined"):
        service.calculate_fee(VehicleCategory.TRUCK, timedelta(hours=1))