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
- just does something and has no Sentry stuff in it whatsoever.
- just inits the sdk and does NOT throw any errors
- has no Sentry stuff and throws an error
- inits the sdk and throws an error
- inits the sdk and starts lots of transactions each containing lots of spans. (100? 500?)
"""


@app.route("/")
def index():
    return {"hello": "world"}


@app.route("/boom")
def boom():
    request = app.current_request
    trigger = int(
        request.query_params["trigger"]
        if request.query_params and "trigger" in request.query_params
        else 0
    )

    return {"hello": boom_util(trigger)}


@app.route("/invoke")
def invoke():
    import boto3
    import json

    request = app.current_request
    trigger = int(
        request.query_params["trigger"]
        if request.query_params and "trigger" in request.query_params
        else 1
    )

    event = {
        "trigger": trigger,
    }

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
    import pandas as pd

    d = {"col1": [1, 2], "col2": [3, 4]}
    df = pd.DataFrame(data=d)

    val = str(df.sum().sum())

    # producing an error
    bla = 10 / event["trigger"]

    return {"value": val}
