from datetime import date
# from views import *


# front controller
def secret_front(request):
    request['date'] = date.today()
    request['year'] = date.today().year


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

# routes = {
#     '/': About(),
#     '/admin/': AdminPanel(),
#     '/orders/': Orders(),
#     '/contacts/': Contacts(),
#     '/cars-list/': CarsList(),
#     '/create-car/': CreateCar(),
#     '/create-classcar/': CreateClassCar(),
#     '/classcar-list/': ClassCarList(),
#     '/copy-car/': CopyCar()
# }
