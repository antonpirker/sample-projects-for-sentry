import base64
import binascii
import os

import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration

from my_routes.routes import boom
from starlette.applications import Starlette
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
)
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", None),
    environment=os.getenv("ENV", "local"),
    integrations=[
        StarletteIntegration(),
    ],
    debug=True,
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)


async def home(request):
    """
    curl --cookie "REQ_TYPE=home" http://localhost:8000/
    """
    return JSONResponse({"hello": "home world"})


async def debug_sentry(request):
    """
    curl --cookie "REQ_TYPE=debug-sentry" http://localhost:8000/debug-sentry
    """
    bla = 1 / 0
    return JSONResponse({"debug_sentry": "true"})


async def upload_something(request):
    """ """
    bla = 1 / 0
    return JSONResponse({"upload": "hello"})


async def post_something(request):
    """
    curl -X POST http://localhost:8000/post --cookie "REQ_TYPE=form" -H "Content-Type: application/x-www-form-urlencoded" -d "username=grace_hopper_form&password=welcome123"
    curl -X POST http://localhost:8000/post --cookie "REQ_TYPE=json" -H "Content-Type: application/json" -d '{"username":"grace_hopper_json","password":"welcome123"}'
    curl -X POST http://localhost:8000/post --cookie "REQ_TYPE=post" -F username=grace_hopper_post -F password=hello123
    """
    form = await request.form()
    bla = 1 / 0
    return JSONResponse({"message": f"Your name is {form['name']}"})


async def membersonly(request):
    """
    curl --cookie "REQ_TYPE=anonymous" http://localhost:8000/members-only/123
    curl --cookie "REQ_TYPE=logged-in" -u 'grace_hopper_basic:welcome123' http://localhost:8000/members-only/123
    """
    if request.user.is_authenticated:
        bla = 1 / 0
        return PlainTextResponse("Hello, " + request.user.display_name)
    return PlainTextResponse("Hello, you are not invited!")


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != "basic":
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError("Invalid basic auth credentials")

        username, _, password = decoded.partition(":")

        # TODO: You'd want to verify the username and password here.

        return AuthCredentials(["authenticated"]), SimpleUser(username)


routes = [
    Route("/", home),
    Route("/debug-sentry", debug_sentry),
    Route("/upload/{rest_of_path:path}", upload_something, methods=["POST"]),
    Route("/post", post_something, methods=["POST"]),
    Route("/members-only/{member_id:int}", membersonly),
]

middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend()),
]

app = Starlette(debug=True, routes=routes, middleware=middleware)
