# Let's get this party started!
from wsgiref.simple_server import make_server

import os
import time

import falcon
import sentry_sdk
from sentry_sdk.integrations.falcon import FalconIntegration

sentry_sdk.init(
   dsn=os.environ.get('SENTRY_DSN', None),
   integrations=[FalconIntegration()]
)

api = falcon.API()

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class ThingsResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override

        time.sleep(2)

        # This is the error that Sentry is capturing.
        bla = 1/0

        resp.text = ('Hello, World')

app = falcon.API()

# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/', things)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')

        # Serve until process is killed
        httpd.serve_forever()
