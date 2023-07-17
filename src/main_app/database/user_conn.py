from sqlalchemy import select
from sqlalchemy.orm import Session

from models import User
import schemas


def get_user(db: Session, user_id: int):
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_name(db: Session, user_name: str):
    stmt = select(User).where(User.username == user_name)
    return db.execute(stmt).scalar_one_or_none()


def create_user(db: Session, user: schemas.UserBase):
    db_user = User(username=user.username,
                   email=user.email,
                   phone=user.phone,
                   first_name=user.first_name,
                   last_name=user.last_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    stmt = select(User).where(User.id == user_id)
    db_user = db.execute(stmt).scalar_one_or_none()
    if db_user:
        to_update = user_update.dict(exclude_unset=True, exclude_defaults=True)
        if to_update:
            for key, value in to_update.items():
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    stmt = select(User).where(User.id == user_id)
    db_user = db.execute(stmt).scalar_one_or_none()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
