import logging
import random

from fastapi import Depends, Request
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

import schemas
from authorization.jwt_tools import get_token_user_name
from database import user_conn
from database.core import get_db

app = FastAPI()

instrumentator = Instrumentator().instrument(app, latency_lowr_buckets=(0.5, 0.95, 0.99, float("inf")))
instrumentator.expose(app)


def allowed_for_user_id(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get("authorization")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is required")

    request_user_id = int(request.path_params.get('user_id'))
    token_user_name = get_token_user_name(token)
    token_user = user_conn.get_user_by_name(db, user_name=token_user_name)

    if not token_user.id == request_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Current user don't have permission to access")


@app.get("/")
async def hello():
    return 'Welcome to my app!'


@app.post("/signup/", response_model=schemas.User)
async def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    try:
        created_user = user_conn.create_user(db=db, user=user)
        return created_user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")


@app.get("/user/{user_id}", response_model=schemas.User, dependencies=[Depends(allowed_for_user_id)])
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_conn.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/user/{user_id}", response_model=schemas.User, dependencies=[Depends(allowed_for_user_id)])
async def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = user_conn.update_user(db=db, user_id=user_id, user_update=user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@app.delete("/user/{user_id}", response_model=schemas.User, dependencies=[Depends(allowed_for_user_id)])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_conn.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Для тестирования сбора статистики прометеем
@app.get("/api/test-1/")
async def test_1():
    handling_time = random.random()
    if handling_time > 0.9:
        raise HTTPException(status_code=500, detail="test exception")

    from asyncio import sleep
    await sleep(handling_time)
    return "ok"


# Для тестирования сбора статистики прометеем
@app.get("/api/test-2/")
async def test_2():
    handling_time = random.random()
    from asyncio import sleep
    await sleep(handling_time)
    if handling_time > 0.8:
        raise HTTPException(status_code=500, detail="test exception")
    return "ok"


@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
