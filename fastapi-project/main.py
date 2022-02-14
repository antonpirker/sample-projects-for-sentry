from calendar import c
import os

from typing import Optional

from fastapi import FastAPI

import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", None),
    environment=os.getenv("ENV", "local"),
)

# import ipdb
# ipdb.set_trace()

app = FastAPI()
asgi_app = SentryAsgiMiddleware(app)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/boom")
async def read_root():
    bla = 1 / 0
    return {"Hello": "Boom (should not be visisble)"}
