"""
It is a way to provide one and only one object of a particular type.
 It involves only one class to create methods and specify the objects.
"""

class Singleton(type):
    _shared_state = {}

    def __init__(self, name, bases, dict):
        print("meta_init")

    def __call__(cls,*args, **kwargs):
        print("__call__")
        # object() is shorthand for object.__call__()
        if cls not in cls._shared_state:
            cls._shared_state[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._shared_state[cls]


class Sample(metaclass=Singleton):
    def __init__(self):
        print("Sample_init")

s1 = Sample()
s2 = Sample()

print(id(s1) == id(s2))

# meta_init
# __call__
# Sample_init
# __call__
# True
