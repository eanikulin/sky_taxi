from copy import deepcopy
from quopri import decodestring
from .behavioral_patterns import FileWriter, Subject
from sqlite3 import connect
from .architectural_system_pattern_unit_of_work import DomainObject


# абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name


# пассажир
class Passenger(User, DomainObject):
    def __init__(self, name):
        super().__init__(name)


# водитель такси
class Driver(User, DomainObject):

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

class DriverMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'driver'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            driver = Driver(name)
            driver.id = id
            result.append(driver)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Driver(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = connect('patterns.sqlite')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'driver': DriverMapper,
    }

    @staticmethod
    def get_mapper(obj):

        if isinstance(obj, Driver):

            return DriverMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')