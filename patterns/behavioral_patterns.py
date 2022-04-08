from jsonpickle import dumps, loads
from sky_framework.templator import render


# поведенческий паттерн - наблюдатель
# Курс
class Observer:

    def update(self, subject):
        pass


class Subject:

    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SmsNotifier(Observer):

    def update(self, subject):
        print('SMS->', 'к управлению авто допущен', subject.drivers[-1].name)


class EmailNotifier(Observer):

    def update(self, subject):
        print(('EMAIL->', 'к управлению авто допущен', subject.drivers[-1].name))


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)


# поведенческий паттерн - Шаблонный метод
class TemplateView:
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self, request):
        template_name = self.get_template()
        context = self.get_context_data()
        data = {}
        data['date'] = request.get('date', None)
        data['year'] = request.get('year', None)
        context['data'] = data
        print(context)
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context(request)


class ListView(TemplateView):
    title = ''
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        context['title'] = self.title
        return context


class CreateView(TemplateView):
    template_name = 'create.html'
    title = ''

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context(request)
        else:
            return super().__call__(request)


# поведенческий паттерн - Стратегия
class ConsoleWriter:

    def write(self, text):
        print(text)


class FileWriter:

    def __init__(self):
        self.file_name = 'log'

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')
