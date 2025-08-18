# Python Cheat Sheet: Concepts, Syntax & Reminders

## Overview

> This cheat sheet summarizes essential Python concepts, syntax, and practical reminders for interviews and daily coding. Each section covers what, why, and how to use core Python features.

---

## Data Structures

### Sets
**What:** Unordered collection of unique elements.
**Why:** Fast membership tests, removing duplicates.
**How:**
```python
my_set = {1, 2, 3}
my_set.add(4)
my_set.remove(2)
```

### Dictionaries
**What:** Key-value pairs, fast lookups.
**Why:** Store and retrieve data by key efficiently.
**How:**
```python
my_dict = {'a': 1, 'b': 2}
my_dict['c'] = 3
value = my_dict.get('a')
```

### Lists
**What:** Ordered, mutable sequence.
**Why:** Store collections, easy to modify.
**How:**
```python
my_list = [1, 2, 3]
my_list.append(4)
my_list[0] = 10
```

### Tuples
**What:** Ordered, immutable sequence.
**Why:** Fixed data, hashable, can be dict keys.
**How:**
```python
my_tuple = (1, 2, 3)
```

---

## Dataclasses
**What:** Classes for storing structured data with less boilerplate.
**Why:** Auto-generates `__init__`, `__repr__`, `__eq__`, and more, making code cleaner and easier to maintain.
**How:**
```python
from dataclasses import dataclass

# 1. Define a dataclass
@dataclass
class Point:
    x: int
    y: int

# 2. Create instances
p1 = Point(1, 2)
p2 = Point(x=3, y=4)

# 3. Access fields
print(p1.x)  # 1
print(p2.y)  # 4

# 4. Comparison and representation
print(p1)         # Point(x=1, y=2)
print(p1 == Point(1, 2))  # True

# 5. Default values
@dataclass
class User:
    name: str
    active: bool = True

u = User("Alice")
print(u)  # User(name='Alice', active=True)

# 6. Type hints and optional fields
from typing import Optional

@dataclass
class Book:
    title: str
    author: Optional[str] = None

b = Book("Python 101")
print(b)  # Book(title='Python 101', author=None)
```

**Summary:**
- Use `@dataclass` above a class definition.
- Define fields with type hints.
- Instantiation is simple: `obj = ClassName(field1, field2)`.
- Fields can have default values and type hints.
- Dataclasses provide readable string representations and easy comparisons.
```

---

## Loops
### For loop
```python
for i in range(5):
    print(i)
```

**While loop:**
```python
count = 0
while count < 5:
    print(count)
    count += 1
```

---

### Looping Through Data Structures

**List:**
```python
my_list = [1, 2, 3]
for item in my_list:
    print(item)
```

**Tuple:**
```python
my_tuple = (1, 2, 3)
for item in my_tuple:
    print(item)
```

**Set:**
```python
my_set = {1, 2, 3}
for item in my_set:
    print(item)
```

**Dictionary (keys):**
```python
my_dict = {'a': 1, 'b': 2}
for key in my_dict:
    print(key)
```

**Dictionary (values):**
```python
for value in my_dict.values():
    print(value)
```

**Dictionary (key-value pairs):**
```python
for key, value in my_dict.items():
    print(f"{key}: {value}")
```

---

## Functions & Testing
**Define a function:**
```python
def add(a, b):
    return a + b
```

### Simple Assertion Test
```python
def test_add():
    assert add(2, 3) == 5

# Call the test directly by invoking the function:
test_add()  # If assertion fails, you'll get an AssertionError

# You can call this in a script, notebook, or interactive shell:
#
# >>> test_add()
# (No output if the test passes)
# >>> test_add()
# Traceback (most recent call last):
#   ...
# AssertionError

# You can also call multiple test functions in a row:
def test_subtract():
    assert (5 - 2) == 3

test_add()
test_subtract()
```

---

## Exception Handling
**Try/Except:**
```python
try:
    x = 1 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

---

## Quick Reference
- Use `set()` for unique items
- Use `dict()` for key-value storage
- Use `list()` for ordered, mutable data
- Use `tuple()` for ordered, immutable data
- Use `@dataclass` for simple data containers
- Use `for` and `while` for iteration
- Use `def` to define functions
- Use `assert` for simple tests
- Use `try/except` for error handling
