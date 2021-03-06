import os

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from fastapi import FastAPI, Form

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", None),
    environment=os.getenv("ENV", "local"),
    integrations=[
        StarletteIntegration(),
        FastApiIntegration(),
    ],
    debug=True,
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)

app = FastAPI(debug=True)

from fastapi import FastAPI, Request


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    return response


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/boom")
async def read_root():
    bla = 1 / 0
    return {"Hello": "Boom (should not be visisble)"}


# broken
@app.post("/my-post")
async def my_post(name: str = Form()):
    bla = 1 / 0
    return {"message": f"Your name is {name}"}
