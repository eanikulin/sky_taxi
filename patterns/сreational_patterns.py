from copy import deepcopy
from quopri import decodestring
from .behavioral_patterns import FileWriter, Subject


# абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name


# пассажир
class Passenger(User):
    pass


# водитель такси
class Driver(User):

    def __init__(self, name):
        self.cars = []
        super().__init__(name)

# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'driver': Driver,
        'passenger': Passenger
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# порождающий паттерн Прототип
class CarPrototype:
    # прототип автомобилей

    def clone(self):
        return deepcopy(self)


class Car(CarPrototype, Subject):

    def __init__(self, name, classcar):
        self.name = name
        self.classcar = classcar
        self.classcar.cars.append(self)
        self.drivers = []
        super().__init__()

    def __getitem__(self, item):
        return self.drivers[item]

    def add_driver(self, driver: Driver):
        self.drivers.append(driver)
        driver.cars.append(self)
        self.notify()

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
    def create_user(type_, name):
        return UserFactory.create(type_, name)

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

    def get_driver(self, name) -> Driver:
        for item in self.drivers:
            if item.name == name:
                return item

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

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)
