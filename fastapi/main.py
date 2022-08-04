import os
import secrets

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from fastapi import FastAPI, Form, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials


sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", None),
    environment=os.getenv("ENV", "local"),
    integrations=[
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

security = HTTPBasic()


@app.get("/")
async def home():
    """
    curl --cookie "REQ_TYPE=home" http://localhost:8000/
    """
    return {"Hello": "Home World"}


@app.get("/debug-sentry")
async def debug_sentry():
    """
    curl --cookie "REQ_TYPE=debug-sentry" http://localhost:8000/debug-sentry
    """
    return {"debug_sentry": "true"}


@app.post("/post")
async def post(username: str = Form(), password: str = Form()):
    """
    curl -X POST http://localhost:8000/post --cookie "REQ_TYPE=form" -H "Content-Type: application/x-www-form-urlencoded" -d "username=grace_hopper_form&password=welcome123"
    curl -X POST http://localhost:8000/post --cookie "REQ_TYPE=json" -H "Content-Type: application/json" -d '{"username":"grace_hopper_json","password":"welcome123"}'
    curl -X POST http://localhost:8000/post --cookie "REQ_TYPE=post" -F username=grace_hopper_post -F password=hello123
    """
    bla = 1 / 0
    return {"message": f"Your name is {username}"}


def _get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username, "grace_hopper_basic"
    )
    correct_password = secrets.compare_digest(credentials.password, "welcome123")
    if not (correct_username and correct_password):
        bla = 1 / 0
    return credentials.username


@app.get("/members-only/{member_id}")
async def members_only(member_id: int, username: str = Depends(_get_current_username)):
    """
    curl --cookie "REQ_TYPE=anonymous" http://localhost:8000/members-only/123
    curl --cookie "REQ_TYPE=logged-in" -u 'grace_hopper_basic:welcome123' http://localhost:8000/members-only/123
    """
    if username:
        bla = 1 / 0
        return {"message": f"Hello, {username} (id: {member_id})"}
    return {"message": "Hello, you are not invited!"}
