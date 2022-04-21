import os
import time

import sentry_sdk
from chalice import Chalice

from chalicelib.utils import boom as boom_util

APP_NAME = "helloworld"

DSN = os.environ.get("SENTRY_DSN", None)
ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT", "dev")
RELEASE = os.environ.get("SENTRY_RELEASE", f"{APP_NAME}@0.0.0")
TRACES_SAMPLE_RATE = float(os.environ.get("SENTRY_TRACE_SAMPLE_RATE", "1.0"))

sentry_sdk.init(
    dsn=DSN,
    environment=ENVIRONMENT,
    release=RELEASE,
    traces_sample_rate=TRACES_SAMPLE_RATE,
)

app = Chalice(app_name=APP_NAME)

"""
- BASELINE (with sentry removed from the code and not layer)
    - measure /
    - measure /boom?trigger=1
    - measure /intrumentation
- CURRENT SENTRY INTEGRATION (call init() and production layer added)
    - measure /
    - measure /boom?trigger=1
    - measure /intrumentation
- NEW EXTENSION (call init and new layer with extension added)
    - measure /
    - measure /boom?trigger=1
    - measure /intrumentation
"""


@app.route("/")
def index():
    """Dummy endpoint doing not much"""

    time.sleep(0.03)

    return {"hello": "world"}


@app.route("/boom")
def boom():
    """Endpoint that can trigger an error"""
    request = app.current_request
    trigger = int(
        request.query_params["trigger"]
        if request.query_params and "trigger" in request.query_params
        else 0
    )

    time.sleep(0.03)

    return {"hello": boom_util(trigger)}


@app.route("/instrumentation")
def instrumentation():
    """Endpoint with lots of custom instrumentation"""

    time.sleep(0.03)

    return {"hello": "instrumentation"}


@app.route("/invoke")
def invoke():
    """Function that can invoke the other Lambda function"""
    import boto3
    import json

    # getting the trigger for raising an error
    request = app.current_request
    trigger = int(
        request.query_params["trigger"]
        if request.query_params and "trigger" in request.query_params
        else 1
    )

    event = {
        "trigger": trigger,
    }

    # invoke the other lambda function
    lambda_client = boto3.client("lambda")
    invoke_response = lambda_client.invoke(
        FunctionName=f"{APP_NAME}-{ENVIRONMENT}-do_important_calculation",
        InvocationType="RequestResponse",
        Payload=json.dumps(event),
    )

    resp = json.loads(invoke_response["Payload"].read())
    print(resp)

    return {"invocation_response": resp["value"]}


@app.lambda_function()
def do_important_calculation(event, context):
    """A second lambda function that can trigger an error

    Using pandas here, because it is a huge lib that takes some time and resources to load."""
    import pandas as pd

    d = {"col1": [1, 2], "col2": [3, 4]}
    df = pd.DataFrame(data=d)

    val = str(df.sum().sum())

    # producing an error
    bla = 10 / event["trigger"]

    return {"value": val}
