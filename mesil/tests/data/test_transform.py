import numpy as np

from mesil.data.process import process_data
from mesil.data.transform import add_tga_weight, percentage_by_first_value


def test_percentage_by_first_value():
    test_array = np.linspace(1, 1000, 1)
    divided_array = percentage_by_first_value(test_array)
    np.testing.assert_equal(
        actual=divided_array, desired=(test_array / test_array[0]) * 100
    )


def test_add_tga_weight(tga_test_file):
    test_data = process_data(tga_test_file)
    add_tga_weight(test_data)
    assert test_data.shape[1] == 5
