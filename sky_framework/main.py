from quopri import decodestring
from .requests import GetRequests, PostRequests
import codecs
import datetime
import json

class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:

    """Класс Framework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        path = environ['PATH_INFO']

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = Framework.decode_value(data)
            print(f'Нам пришёл post-запрос: {Framework.decode_value(data)}')
            Framework.get_message(request['data'])
            Framework.get_message_json(request['data'])
        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = Framework.decode_value(request_params)
            print(f'Нам пришли GET-параметры:'
                  f' {Framework.decode_value(request_params)}')

        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()
        request = {}
        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts_lst:
            front(request)
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data

    @staticmethod
    def get_message(message):
        with codecs.open(f'{message["first_name"]}.txt', 'a', 'UTF-8') as message_file:
            message_file.write(f'--------------{datetime.datetime.now()}--------------' + '\n')
            message_file.write(f'Имя пользователя: {message["first_name"]}'+'\n')
            message_file.write(f'Email: {message["email"]}'+'\n')
            message_file.write(f'Тема сообщения: {message["message_title"]}'+'\n')
            message_file.write(f'Текст обращения: {message["message_text"]}'+'\n')
            message_file.write(f'------------------------------------------------------' + '\n')

    @staticmethod
    def get_message_json(message):
        with codecs.open(f'{message["first_name"]}.json', 'w', 'UTF-8') as message_file:
            message['data'] = str(datetime.datetime.now())
            json.dump(message, message_file, ensure_ascii=False)



