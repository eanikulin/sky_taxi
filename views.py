from sky_framework.templator import render
from patterns.сreational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug

site = Engine()
logger = Logger('main')
routes = {}

def context(request):return {'date': request.get('date', None), 'year': request.get('year', None)}

@AppRoute(routes=routes, url='/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        data = context(request)
        data['title'] = 'О нас - Sky Taxi'
        return '200 OK', render('index.html', data=data, objects_list=site.classescars)

@AppRoute(routes=routes, url='/admin/')
class AdminPanel:
    @Debug(name='AdminPanel')
    def __call__(self, request):
        data = context(request)
        data['title'] = 'Административная панель - Sky Taxi'
        return '200 OK', render('admin.html', data=data, objects_list=site.classescars)

# контроллер 404
class NotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - список автомобилей
@AppRoute(routes=routes, url='/cars-list/')
class CarsList:
    @Debug(name='CarsList')
    def __call__(self, request):
        data = context(request)
        data['title'] = 'Список автомобилей'
        logger.log('Список автомобилей')
        try:
            classcar = site.find_classcar_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('car_list.html',
                                    objects_list=classcar.cars,
                                    name=classcar.name, id=classcar.id, data=data)
        except KeyError:
            return '200 OK', 'No cars have been added yet'


# контроллер - создать авто
@AppRoute(routes=routes, url='/create-car/')
class CreateCar:
    classcar_id = -1

    @Debug(name='CreateCar')
    def __call__(self, request):
        data = context(request)
        data['title'] = 'Создание авто'
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            classcar = None
            if self.classcar_id != -1:
                classcar = site.find_classcar_by_id(int(self.classcar_id))

                car = site.create_car('passenger', name, classcar)
                site.cars.append(car)

            return '200 OK', render('car_list.html',
                                    objects_list=classcar.cars,
                                    name=classcar.name,
                                    id=classcar.id, data=data)

        else:
            try:
                self.classcar_id = int(request['request_params']['id'])
                classcar = site.find_classcar_by_id(int(self.classcar_id))

                return '200 OK', render('create_car.html',
                                        name=classcar.name,
                                        id=classcar.id, data=data)
            except KeyError:
                return '200 OK', 'No classescars have been added yet'


# контроллер - создать класс авто
@AppRoute(routes=routes, url='/create-classcar/')
class CreateClassCar:

    @Debug(name='CreateClassCar')
    def __call__(self, request):
        data = context(request)
        data['title'] = 'Создание класса'

        if request['method'] == 'POST':
            # метод пост

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            classcar_id = data.get('classcar_id')

            classcar = None
            if classcar_id:
                classcar = site.find_classcar_by_id(int(classcar_id))

            new_classcar = site.create_classcar(name, classcar)

            site.classescars.append(new_classcar)

            return '200 OK', render('admin.html', objects_list=site.classescars, data=data)
        else:
            classescars = site.classescars
            return '200 OK', render('create_classcar.html',
                                    classescars=classescars, data=data)


# контроллер - список классов авто
@AppRoute(routes=routes, url='/classcar-list/')
class ClassCarList:

    @Debug(name='ClassCarList')
    def __call__(self, request):
        logger.log('Список классов авто')
        data = context(request)
        data['title'] = 'Список классов авто'
        return '200 OK', render('classcar_list.html',
                                objects_list=site.classescars, data=data)


# контроллер - копировать авто
@AppRoute(routes=routes, url='/copy-car/')
class CopyCar:

    @Debug(name='CopyCar')
    def __call__(self, request):
        data = context(request)
        data['title'] = 'Список классов авто'
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_car = site.get_car(name)
            if old_car:
                new_name = f'copy_{name}'
                new_car = old_car.clone()
                new_car.name = new_name
                site.cars.append(new_car)

            return '200 OK', render('car_list.html',
                                    objects_list=site.cars,
                                    name=new_car.classcar.name, data=data)
        except KeyError:
            return '200 OK', 'No cars have been added yet'

@AppRoute(routes=routes, url='/orders/')
class Orders:

    @Debug(name='Orders')
    def __call__(self, request):
        data = context(request)
        data['title'] = 'Заказы - Sky Taxi'
        return '200 OK', render('orders.html', data=data)

@AppRoute(routes=routes, url='/contacts/')
class Contacts:

    @Debug(name='Contacts')
    def __call__(self, request):
        data = context(request)
        data['title'] = 'Контакты - Sky Taxi'
        return '200 OK', render('contacts.html', data=data)
