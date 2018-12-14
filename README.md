# pover
Python Overloading Methods

## Install
```
pip3 install pover
```

## Example
Declare your class with metaclass `pover.OverloadMeta`

```
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
