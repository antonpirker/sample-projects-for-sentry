import os

import sentry_sdk
from sentry_sdk.integrations.quart import QuartIntegration

from quart import Quart, render_template, websocket

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", None),
    environment=os.getenv("ENV", "local"),    
    integrations=[
       QuartIntegration(),
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)


app = Quart(__name__)


@app.route("/")
async def hello():
    return await render_template("./index.html")


@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0


@app.websocket("/debug-sentry-ws")
async def trigger_error_ws():
    division_by_zero = 1 / 0


@app.route("/api")
async def json():
    return {"hello": "world"}


@app.websocket("/ws")
async def ws():
    while True:
        await websocket.send("hello")
        await websocket.send_json({"hello": "world"})


if __name__ == "__main__":
    app.run()
