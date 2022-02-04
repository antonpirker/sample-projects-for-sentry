from quart import Quart

import sentry_sdk

sentry_sdk.init(traces_sample_rate=1.0, send_default_pii=True, debug=True)

app = Quart(__name__)


@app.route("/")
async def index():
    return "Hello World"


@app.route("/error")
async def error():
    raise ValueError("Something strange going on!")


if __name__ == "__main__":
    app.run()
