from datetime import date
from views import About, Contacts, Orders


# front controller
def secret_front(request):
    request['date'] = date.today()
    request['year'] = date.today().year


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': About(),
    '/orders/': Orders(),
    '/contacts/': Contacts(),
}
