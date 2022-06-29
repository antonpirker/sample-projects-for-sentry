import os
from calendar import c

from fastapi import FastAPI

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", None),
    environment=os.getenv("ENV", "local"),
    integrations=[
        FastApiIntegration(
            transaction_style="url",
        ),
    ],
    debug=True,
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)

# import ipdb
# ipdb.set_trace()

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/boom")
async def read_root():
    bla = 1 / 0
    return {"Hello": "Boom (should not be visisble)"}
