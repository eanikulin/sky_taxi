from copy import deepcopy
from quopri import decodestring


# абстрактный пользователь
class User:
    pass


# пассажир
class Passenger(User):
    pass


# водитель такси
class Driver(User):
    pass


class UserFactory:
    types = {
        'driver': Driver,
        'passenger': Passenger
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


# порождающий паттерн Прототип
class CarPrototype:
    # прототип автомобилей

    def clone(self):
        return deepcopy(self)


class Car(CarPrototype):

    def __init__(self, name, classcar):
        self.name = name
        self.classcar = classcar
        self.classcar.cars.append(self)


# грузовой
class Truck(Car):
    pass


# легковой
class PassengerCar(Car):
    pass

# автобус
class Bus(Car):
    pass


class CarFactory:
    types = {
        'truck': Truck,
        'passenger': PassengerCar,
        'bus': Bus
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, classcar):
        return cls.types[type_](name, classcar)


# класс авто
class ClassCar:
    auto_id = 0

    def __init__(self, name, classcar):
        self.id = ClassCar.auto_id
        ClassCar.auto_id += 1
        self.name = name
        self.classcar = classcar
        self.cars = []

    def car_count(self):
        result = len(self.cars)
        if self.classcar:
            result += self.classcar.car_count()
        return result


# основной интерфейс проекта
class Engine:
    def __init__(self):
        self.passengers = []
        self.drivers = []
        self.cars = []
        self.classescars = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_classcar(name, classcar=None):
        return ClassCar(name, classcar)

    def find_classcar_by_id(self, id):
        for item in self.classescars:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет класса авто с id = {id}')

    @staticmethod
    def create_car(type_, name, classcar):
        return CarFactory.create(type_, name, classcar)

    def get_car(self, name):
        for item in self.cars:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
