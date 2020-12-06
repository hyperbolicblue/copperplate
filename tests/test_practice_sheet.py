# -*- coding: utf-8 -*-
# author: hyperbolicblue <hyperbolicblue@protonmail.com>
#
# This file is licensed under: BSD 3-Clause License.
# Copyright (c) 2020, hyperbolicblue <hyperbolicblue@protonmail.com>
# All rights reserved.
# See <https://github.com/hyperbolicblue/copperplate>

import pytest
from scripts import practice_sheet as ps
from pathlib import Path


def test_raise_OSError_if_file_exists_without_using_force():
    filename = 'existingfile.pdf'
    Path(filename).touch()
    with pytest.raises(OSError) as e_info:
        ps.parse_args([filename])
    Path(filename).unlink()


def test_raise_ValueError_if_slantangle_too_small():
    for testangle in [-4, -3, -2, -1, 0.1, 1, 2, 3, 4, 359, 363]:
        with pytest.raises(ValueError) as e_info:
            ps.parse_args(['-s', str(testangle), 'filename.pdf'])
