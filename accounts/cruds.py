from sqlalchemy.orm import Session
from fastapi import HTTPException , status
from . import models, schemas
from .utils import Hash


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserRegister):
    hashed_password = Hash.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update(db: Session, user: schemas.UpdateUser , id:int):

    # get the existing data
    db_user = db.query(models.User).filter(models.User.id == id).one_or_none()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found")

    # Update model class variable from requested fields # **typo** was vars(db_user) => vars(user)
    for var, value in vars(user).items():
        setattr(db_user, var, value) if value else None

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def destroy(id:int,db: Session):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found")

    user.delete(synchronize_session=False)
    db.commit()
