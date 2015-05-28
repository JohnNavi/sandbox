#!/usr/bin/env python

from mul import multi

def test_numbers_3_4():
    assert multi(3,4) == 12

def test_strings_a_3():
    assert multi('a',3) == 'aaa'

def test_intentional_fail():
    assert multi(2,2) == 6


