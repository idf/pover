#!/usr/bin/env python3
import unittest
import pover

class Bar:
    def __init__(self):
        self.number = 100

class Foo(metaclass=pover.OverloadMeta):
    def add(self, a: int):
        return a + 1

    def add(self, a: str):
        return a + " world"

    def add(self, a: float):
        return a + 0.1

    def add(self, a: Bar):
        return a.number + 1

    def add(self, a: list):
        return a + [1]

    def add(self, a: set):
        a.add(1)
        return a

    def minus(self, a: int):
        return a - 1

    def minus(self, a: str):
        return a[:-1]

class OverloadTest(unittest.TestCase):
    def test_overload(self):
        foo = Foo()
        self.assertEqual(foo.add(1), 2)
        self.assertEqual(foo.add("hello"), "hello world")
        self.assertEqual(foo.add(0.1), 0.2)
        self.assertEqual(foo.add(Bar()), 101)
        self.assertEqual(foo.add([0]), [0, 1])
        self.assertEqual(foo.add({0}), {0, 1})
        self.assertEqual(foo.minus(1), 0)
        self.assertEqual(foo.minus("hello"), "hell")
