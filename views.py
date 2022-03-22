from sky_framework.templator import render


def context(request):return {'date': request.get('date', None), 'year': request.get('year', None)}

class About:
    def __call__(self, request):
        data = context(request)
        data['title'] = 'О нас - Sky Taxi'
        return '200 OK', render('index.html', data=data)


class Orders:
    def __call__(self, request):
        data = context(request)
        data['title'] = 'Заказы - Sky Taxi'
        return '200 OK', render('orders.html', data=data)


class Contacts:
    def __call__(self, request):
        data = context(request)
        data['title'] = 'Контакты - Sky Taxi'
        return '200 OK', render('contacts.html', data=data)
