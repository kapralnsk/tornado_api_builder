# BEWARE this project is unfinished, and dead

# Tornado API Builder

Allows you to easily create RESTful HTTP API, based on Tornado web framework.

## Usage

Write logic for your API

```python
from tornado-api_builder import RESTResource

class HelloWorldResource(RESTResource):
    path = 'hello_world/'

    def get(self, world_name):
        return {'message': 'hello {}'.format(world_name)}
```

Then import all resource classes in your server.py and create a router

```python
import tornado.web
from tornado-api_builder import RESTRouter

router = RESTRouter()
router.register(HelloWorldResource)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = router.urls
```

Then your handler should be accessible at ```api/hello_world/```.

## Limitations
1. Resource versioning is not supported - you should create a new Resource for new resource version.
2. Resource handlers should only return dictionary - which then returns to client as a JSON.
