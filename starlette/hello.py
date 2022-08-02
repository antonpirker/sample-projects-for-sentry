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


async def homepage(request):
    return JSONResponse({"hello": "world"})


async def debug_sentry(request):
    bla = 1 / 0


async def upload_something(request):
    bla = 1 / 0
    return JSONResponse({"upload": "hello"})


async def auth(request):
    bla = 1 / 0
    if request.user.is_authenticated:
        return PlainTextResponse("Hello, " + request.user.display_name)
    return PlainTextResponse("Hello, you are not invited!")


async def my_post(request):
    form = await request.form()
    bla = 1 / 0
    return JSONResponse({"message": f"Your name is {form['name']}"})


def my_post2(request):
    form = request.form()
    bla = 1 / 0
    return JSONResponse({"message": f"Your name is {form['name']}"})


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
    Route("/", homepage),
    Route("/some_url", debug_sentry),
    Route("/membersonly/{my_id:int}", auth),
    Route("/float/{number:float}", boom),
    Route("/upload/{rest_of_path:path}", upload_something, methods=["POST"]),
    Route("/my-post", my_post, methods=["POST"]),
]

middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend()),
]

app = Starlette(debug=True, routes=routes, middleware=middleware)
