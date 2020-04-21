from abc import ABC, abstractmethod

# product parts
class Wheel:
    def __init__(self, size=0):
        self.size = size

class Engine:
    def __init__(self, horsepower=0):
        self.horsepower = horsepower

class Body:
    def __init__(self, shape='***'):
        self.shape = shape

# car - Product
class Car:
    def __init__(self):
        self.__body = None
        self.__engine = None
        self.__wheels = list()

    def set_body(self, body):
        self.__body = body

    def set_engine(self, engine):
        self.__engine = engine

    def attach_wheels(self, wheel):
        self.__wheels.append(wheel)

    def specification(self):
        print("body: {}".format(self.__body.shape))
        print("engine power: {}".format(self.__engine.horsepower))
        print("tire size: {}\n\n".format(self.__wheels[0].size))

# create variaouse part of vehicle
class Builder(ABC):

    @abstractmethod
    def get_wheel(self):
        pass

    @abstractmethod
    def get_engine(self):
        pass

    @abstractmethod
    def get_body(self):
        pass


#Concrete Builder
class JeepBuilder(Builder):

    def get_wheel(self):
        wheel = Wheel(size=10)
        return wheel

    def get_engine(self):
        engine = Engine(horsepower=100)
        return engine

    def get_body(self):
        body = Body(shape='Jeep')
        return body


class NisanBuilder(Builder):
    def get_wheel(self):
        wheel = Wheel(size=5)
        return wheel

    def get_engine(self):
        engine = Engine(horsepower=101)
        return engine

    def get_body(self):
        body = Body(shape='Nissan')
        return body


#director

class Director:
    __builder = None

    def set_builder(self, builder):
        self.__builder = builder

    def get_car(self):
        body = self.__builder.get_body()
        engine = self.__builder.get_engine()

        car =  Car()
        car.set_body(body)
        car.set_engine(engine)

        for i in range(4):
            wheel = Wheel(size=12)
            car.attach_wheels(wheel)
        return car

def main():
    jeep = JeepBuilder()
    nissan = NisanBuilder()
    director = Director()
    director.set_builder(jeep)
    car1 = director.get_car()
    director.set_builder(nissan)
    car2 = director.get_car()
    car1.specification()
    car2.specification()

if __name__ == '__main__':
    main()
