# Classes & Object-Oriented Programming

## Overview
Python classes for creating reusable, maintainable code with inheritance, encapsulation, and polymorphism.

---

## Basic Class Definition

```python
class Person:
    # Class variable (shared across all instances)
    species = "Homo sapiens"
    
    def __init__(self, name, age=0):
        # Instance variables (unique to each instance)
        self.name = name
        self.age = age
        self._protected = "internal use"  # Convention: protected
        self.__private = "very private"   # Name mangling applied
    
    def greet(self):
        """Instance method - has access to self"""
        return f"Hello, I'm {self.name}"
    
    @classmethod  # Alternative constructor, gets class not instance
    def from_string(cls, person_str):
        """Class method - alternative constructor"""
        name, age = person_str.split('-')
        return cls(name, int(age))
    
    @staticmethod  # Utility function, no access to class or instance
    def is_adult(age):
        """Static method - doesn't need class or instance"""
        return age >= 18

# Usage
person1 = Person("Alice", 25)
person2 = Person.from_string("Bob-30")  # Using class method - parses "name-age" format
print(person1.greet())          # "Hello, I'm Alice"
print(person2.greet())          # "Hello, I'm Bob" 
print(Person.is_adult(25))      # True

# Class method allows different ways to create objects
person3 = Person.from_string("Charlie-35")  # Alternative constructor
print(f"{person3.name} is {person3.age}")   # "Charlie is 35"

# Using inherited methods from object
print(person1)                  # Uses inherited __str__ → <__main__.Person object at 0x...>
print(repr(person1))            # Uses inherited __repr__ → <__main__.Person object at 0x...>
print(person1 == person2)       # Uses inherited __eq__ → False (identity comparison)
```

---

## Inherited Methods from `object`

Every Python class automatically inherits from `object`, which provides default implementations:

### **Always Inherited (Common Overrides)**
- **`__init__(self)`** - Constructor (default does nothing)
- **`__str__(self)`** - User-friendly string (default falls back to `__repr__`)
- **`__repr__(self)`** - Developer string (default: `<__main__.ClassName object at 0x...>`)
- **`__eq__(self, other)`** - Equality check (default: `self is other`)
- **`__hash__(self)`** - Hash for sets/dicts (default: `hash(id(self))`, becomes `None` if `__eq__` overridden)

### **Often Inherited (Less Common Overrides)**
- **`__ne__(self, other)`** - Not equal (default: `not self.__eq__(other)`)
- **`__bool__(self)`** - Truth value (default: `True`, unless `__len__` returns 0)
- **`__len__(self)`** - Length (default: not defined, raises `TypeError`)
- **`__iter__(self)`** - Iterator (default: not defined, raises `TypeError`)
- **`__contains__(self, item)`** - Membership test (default: iterates through `__iter__`)

### **Rarely Overridden (Advanced)**
- **`__new__(cls, *args)`** - Object creation (before `__init__`)
- **`__del__(self)`** - Destructor (default: does nothing)
- **`__getattribute__(self, name)`** - Attribute access (default: normal lookup)
- **`__setattr__(self, name, value)`** - Attribute assignment (default: normal assignment)
- **`__delattr__(self, name)`** - Attribute deletion (default: normal deletion)

### **Key Inheritance Rules**
1. **Override `__eq__`** → Must override `__hash__` if you want hashable objects
2. **Override `__str__`** → Should also override `__repr__` for consistency
3. **Override `__len__`** → `__bool__` automatically returns `len(self) != 0`
4. **Most magic methods** → Not inherited by default, must implement explicitly

---

## Class Methods & Static Methods

**Class Methods (`@classmethod`):**
- Receive the class as first parameter (`cls`) instead of instance (`self`)
- Used for alternative constructors or operations on the class itself
- Can access class variables and create new instances

**Static Methods (`@staticmethod`):**
- Don't receive class or instance as parameter
- Used for utility functions related to the class but independent of state
- Behave like regular functions but grouped with the class for organization

**Example:**
```python
class Temperature:
    unit = "Celsius"  # Class variable
    
    def __init__(self, value):
        self.value = value
    
    @classmethod
    def from_fahrenheit(cls, fahrenheit):
        """Alternative constructor - converts F to C"""
        celsius = (fahrenheit - 32) * 5/9
        return cls(celsius)  # Creates new instance using cls
    
    @classmethod
    def get_unit(cls):
        """Class method accessing class variable"""
        return cls.unit
    
    @staticmethod
    def is_freezing(celsius):
        """Static method - utility function"""
        return celsius <= 0

# Usage
temp1 = Temperature(25)                    # Regular constructor
temp2 = Temperature.from_fahrenheit(77)    # Class method constructor
print(temp2.value)                         # 25.0 (converted from 77°F)
print(Temperature.get_unit())              # "Celsius" (class method)
print(Temperature.is_freezing(-5))        # True (static method)
```

---

## Inheritance

### Single Inheritance
```python
class Employee(Person):  # Employee inherits from Person
    def __init__(self, name, age, employee_id):
        super().__init__(name, age)  # Call parent constructor
        self.employee_id = employee_id
    
    def greet(self):
        """Override parent method"""
        return f"Hello, I'm {self.name}, employee #{self.employee_id}"
    
    def get_info(self):
        """Extend parent method"""
        return f"{super().get_info()}, Employee ID: {self.employee_id}"

# Usage
emp = Employee("Alice", 30, "E123")
print(emp.greet())  # "Hello, I'm Alice, employee #E123"
```

### Multiple Inheritance & MRO (Method Resolution Order)
```python
class Flyable:
    def fly(self):
        return "Flying!"

class Swimmable:
    def swim(self):
        return "Swimming!"

class Duck(Flyable, Swimmable):
    def quack(self):
        return "Quack!"

# Check method resolution order
print(Duck.mro())  
# Prints: [<class '__main__.Duck'>, <class '__main__.Flyable'>, <class '__main__.Swimmable'>, <class 'object'>]
```

---


## Data Classes (Python 3.7+)

**Automatically generates these methods:**
- **`__init__()`** - Constructor from type annotations
- **`__repr__()`** - Developer-friendly string representation  
- **`__eq__()`** - Equality comparison based on all fields
- **`__hash__()`** - Hash function (only if `frozen=True`)

**Example:**
```python
from dataclasses import dataclass

@dataclass(frozen=True)  # frozen=True makes it hashable
class Point:
    x: float
    y: float
    # __init__, __repr__, __eq__, and __hash__ automatically created!

# Usage - both versions work identically
p1 = Point(3, 4)
p2 = Point(3, 4)
print(p1)          # Point(x=3, y=4)  [__repr__]
print(p1 == p2)    # True             [__eq__]
print(hash(p1))    # Some number      [__hash__]
```

---

## Context Managers

Automatically handle resource cleanup (like closing files) even if exceptions occur.

**Required methods for `with` statement:**
- **`__enter__(self)`** - Called when entering `with` block, returns resource
- **`__exit__(self, exc_type, exc_value, traceback)`** - Called when exiting, handles cleanup

**Example:**
```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()
        return False  # Don't suppress exceptions

# Usage
with FileManager("data.txt", "w") as f:
    f.write("Hello, World!")  # File automatically closed after block
```

---

## Class Design Patterns

### Singleton Pattern

Ensures only one instance of a class exists globally, preventing accidental multiple instances when you need exactly one shared object.

**Use cases:** Database connections, loggers, configuration objects, or any resource that should have only one instance globally.

```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.value = 0
            self.initialized = True

# Usage
s1 = Singleton()
s2 = Singleton()
print(s1 is s2)  # True - same instance
```

### Factory Pattern
```python
class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class ShapeFactory:
    @staticmethod
    def create_shape(shape_type, *args, **kwargs):
        if shape_type == "circle":
            return Circle(*args, **kwargs)
        elif shape_type == "rectangle":
            return Rectangle(*args, **kwargs)
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")

# Usage
circle = ShapeFactory.create_shape("circle", 5)  # Circle(radius=5) - positional args
rectangle = ShapeFactory.create_shape("rectangle", width=10, height=5)  # Rectangle(width=10, height=5) - keyword args
print(f"Circle area: {circle.area()}")  # Circle area: 78.53975
print(f"Circle radius: {circle.radius}")  # Circle radius: 5
```

---

## Best Practices

1. **Use `__slots__`** for memory efficiency with many instances:

Restricts objects to only predefined attributes, removing the flexible `__dict__` in favor of fixed memory slots. Use when creating thousands of simple objects where memory usage matters. 

```python
class Point:
    __slots__ = ['x', 'y']  # Restricts attributes, saves memory
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Usage
p = Point(3, 4)
print(p.x, p.y)     # 3 4 - OK, attributes in __slots__
p.z = 5             # AttributeError: 'Point' object has no attribute 'z'
print(p.__dict__)   # AttributeError: 'Point' object has no attribute '__dict__'
```

2. **Type hints** for better code documentation:
```python
from typing import List, Optional

class Calculator:
    def add_numbers(self, numbers: List[float]) -> float:
        return sum(numbers)
    
    def divide(self, a: float, b: float) -> Optional[float]:
        return a / b if b != 0 else None
```

3. **Use descriptors** for reusable attribute validation:
```python
class PositiveNumber:
    def __init__(self, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        return obj.__dict__[self.name]
    
    def __set__(self, obj, value):
        if value <= 0:
            raise ValueError(f"{self.name} must be positive")
        obj.__dict__[self.name] = value

class Product:
    price = PositiveNumber("price")
    weight = PositiveNumber("weight")
    
    def __init__(self, name, price, weight):
        self.name = name
        self.price = price
        self.weight = weight

# Usage - descriptors in action
product = Product("Laptop", 1000, 2.5)
print(product.price)    # 1000 - calls PositiveNumber.__get__()
product.weight = 3.0    # OK - calls PositiveNumber.__set__()
product.price = -50     # ValueError: price must be positive

# Validation during creation
try:
    bad_product = Product("Phone", 500, -1.0)  # ValueError: weight must be positive
except ValueError as e:
    print(f"Error: {e}")  # Error: weight must be positive
```