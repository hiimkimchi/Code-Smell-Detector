# Code-Smell-Detector
Detects if a .py file has methods/parameters that are too verbose or any duplicated code

## Usage
```bash
python3 App.py
```

## Example
```python
def func1(e,f,g):
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    print("hi")
    return e,f,g

def func2(a, b, c, d, e, f, g, h):
    return a

def func3(a, b):
    return a * b

def func4(c, d):
    return c * d
```

<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" />