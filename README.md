# pover
Python OVERloading (pover) methods with type hints

It is equipped with fast method look up, minimal runtime hit, overloading method at class construction time.

## Install
```
pip3 install pover
```

## Example
All you need is `pover.OverloadMeta`. Simply declare your class with metaclass `pover.OverloadMeta`

```py
#!/usr/bin/env python3
import unittest
import pover


class Foo(metaclass=pover.OverloadMeta):
    def add(self, a: int):
        return a + 1

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
        self.assertEqual(foo.add([0]), [0, 1])
        self.assertEqual(foo.add({0}), {0, 1})
        self.assertEqual(foo.minus(1), 0)
        self.assertEqual(foo.minus("hello"), "hell")
```

## Run tests:
```
python3 -m unittest pover.tests.tests
```
