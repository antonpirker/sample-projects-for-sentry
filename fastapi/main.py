import io
import os
import secrets

import sentry_sdk
from PIL import Image
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal
from fastapi import (Depends, FastAPI, File, Form, HTTPException, 
                     UploadFile)
from fastapi.security import HTTPBasic, HTTPBasicCredentials

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", None),
    environment=os.getenv("ENV", "local"),
    traces_sample_rate=1.0,
    send_default_pii=True,
    debug=True,
)

app = FastAPI(debug=True)


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
    bla = 1 / 0
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


security = HTTPBasic()

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


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/shows/", response_model=list[schemas.Show])
def read_shows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shows = crud.get_shows(db, skip=skip, limit=limit)
    return shows


@app.get("/api/shows/{show_id}", response_model=schemas.Show)
def read_show(show_id: int, db: Session = Depends(get_db)):
    show = crud.get_show(db, show_id=show_id)
    if show is None:
        raise HTTPException(status_code=404, detail="Show not found")
    return show


@app.post("/predict")
async def predict(file: UploadFile = File(default=None)):
    contents = await file.read()
    Image.open(io.BytesIO(contents)).convert("RGB")
    return {"result": "ok"}


# @app.middleware("http")
# async def logging_middleware(request: Request, call_next):
#     start_time = time.time()
#     print(f'~~~~~~~ reading request body in logging_middleware')

#     import ipdb
#     ipdb.set_trace()
#     body = await request.body()
#     print(body)
#     response = await call_next(request)
#     return response
