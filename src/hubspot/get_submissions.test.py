// ```python
import pytest

from my_module import calculate_area


def test_calculate_area():
    """Test that the calculate_area function returns the correct area."""

    # Test for a circle
    radius = 10
    expected_area = 314.1592653589793
    actual_area = calculate_area(radius)
    assert actual_area == expected_area

    # Test for a square
    side_length = 10
    expected_area = 100
    actual_area = calculate_area(side_length)
    assert actual_area == expected_area

    # Test for a rectangle
    width = 10
    height = 20
    expected_area = 200
    actual_area = calculate_area(width, height)
    assert actual_area == expected_area
// ```