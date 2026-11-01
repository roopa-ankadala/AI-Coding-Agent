from calculator import add, divide

assert add(2,3) == 5

assert divide(10,2) == 5

try:
    divide(10,0)
    assert False
except ValueError:
    pass

print("All tests passed!")
