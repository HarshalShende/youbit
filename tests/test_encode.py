"""
This file (test_encode.py) contains unit tests for the encode.py file.
"""
from youbit import encode
from pathlib import Path
import os
import numpy as np


def test_lastframe_padding():
    """WHEN we call add_lastframe_padding() with an array of different arguments.
    THEN verify that the returned array's length is divisible by the total pixel count of the passed resolution.
    """
    arrs = [
        np.random.randint(0,256,1000, dtype=np.uint8),
        np.random.randint(0,256,10000000, dtype=np.uint8)
    ]
    resolutions = [(1920,1080), (2560,1440), (3840,2160)]
    bpps = [1,2,3]
    for arr in arrs:
        for res in resolutions:
            for bpp in bpps:
                pixel_count = res[0] * res[1]
                output = encode.add_lastframe_padding(arr, res, bpp)
                assert (output.size % pixel_count) == 0


def test_transform_array(tempdir):
    """WHEN we use the transform_array() function on valid array.
    THEN verify if the returned array is of correct size AND equal to a precalculated and validated array.
    Please note the transform_array() function has exact requirements for the input array's size than need to be followed.
    """
    arr = [i for i in range(256)] * 8100 # makes the length exactly 2073600, or the sum of pixels in a 1920x1080 frame. 

    solution_bpp1 = Path(os.getcwd()) / 'testdata' / 'solutions' / 'test_transform_array_solution_bpp1.npy'
    solution_bpp1 = np.load(str(solution_bpp1))

    solution_bpp2 = Path(os.getcwd()) / 'testdata' / 'solutions' / 'test_transform_array_solution_bpp2.npy'
    solution_bpp2 = np.load(str(solution_bpp2))

    solution_bpp3 = Path(os.getcwd()) / 'testdata' / 'solutions' / 'test_transform_array_solution_bpp3.npy'
    solution_bpp3 = np.load(str(solution_bpp3))

    for bpp in (1,2,3):
        output = encode.transform_array(arr, bpp)
        desired_size = int(arr.size * 8 / bpp)
        assert output.size == desired_size
        if bpp == 1:
            np.testing.assert_array_equal(output, solution_bpp1)
        if bpp == 2:
            np.testing.assert_array_equal(output, solution_bpp2)
        if bpp == 3:
            np.testing.assert_array_equal(output, solution_bpp3)
        else:
            assert False, 'No valid bbp value was detected, thus this test cannot be validated. This is an issue inside this test function.'