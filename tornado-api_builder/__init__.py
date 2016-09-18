from tornado.web import RequestHandler, HTTPError
from tornado.escape import recursive_unicode, json_decode, json_encode


def get_ip(headers):
    x_forwarded_for = headers.get('X-Forwarded-For').split(',')[0] if headers.get('X-Forwarded-For') else None
    ip = headers.get('X-Real-IP') or x_forwarded_for
    if ip == 'unknown':
        return None
    return ip


class _APIHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    @staticmethod
    def get_request_data(request):
        if request.method == 'GET':
            request_data = {key: ''.join(value) for key, value in recursive_unicode(request.arguments.items())}
        else:
            request_data = json_decode(request.body)
        return request_data

    def run_logic(self, func):
        args = set(list(func.__func__.__code__.co_varnames)[1:])
        request_data = self.get_request_data(self.request)

        if 'ip' in args:
            request_data.update({'ip': get_ip(self.request.headers)})

        client_keys = set(request_data.keys())
        missing_arguments = args - client_keys
        if missing_arguments:
            message = 'arguments {} are missing'.format(missing_arguments)
            raise HTTPError(status_code=400, reason=message)

        try:
            response = func(**request_data)
        except Exception as e:
            raise HTTPError(status_code=400, reason=str(e))
        self.write(json_encode(response))

    def get(self, *args, **kwargs):
        logic = self.rest_resource.get
        if logic:
            self.run_logic(logic)

    def post(self, *args, **kwargs):
        logic = self.rest_resource.post
        if logic:
            self.run_logic(logic)


class RESTResource(object):
    path = ''

    def __init__(self):
        if not self.path:
            raise NotImplementedError('specify path to your Resource')

    def get_handler_class(self):
        return type('{}Handler'.format(self.__class__.__name__), (_APIHandler,), {'rest_resource': self})


class RESTRouter(object):
    _resources = []

    def register(self, resource):
        self._resources.append((resource.path, resource().get_handler_class()))

    @property
    def urls(self):
        return list(map(lambda item: (r'api/{}'.format(item[0]), item[1]), self._resources))
