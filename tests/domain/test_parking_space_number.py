
import unittest

from src.domain.value_objects.parking_space_number import (
    ParkingSpaceNumber,
)


class TestParkingSpaceNumber(unittest.TestCase):

    def test_accepts_valid_number(self):
        number = ParkingSpaceNumber("PS-001")
        self.assertEqual(str(number), "PS-001")

    def test_accepts_another_valid_number(self):
        number = ParkingSpaceNumber("PS-025")
        self.assertEqual(number.value, "PS-025")

    def test_rejects_empty_number(self):
        with self.assertRaises(ValueError):
            ParkingSpaceNumber("")

    def test_rejects_letters_only(self):
        with self.assertRaises(ValueError):
            ParkingSpaceNumber("ABC")

    def test_rejects_wrong_digit_count(self):
        with self.assertRaises(ValueError):
            ParkingSpaceNumber("PS-1")

    def test_rejects_extra_characters(self):
        with self.assertRaises(ValueError):
            ParkingSpaceNumber("PS-001X")

    def test_rejects_non_string_value(self):
        with self.assertRaises(ValueError):
            ParkingSpaceNumber(123)


if __name__ == "__main__":
    unittest.main()