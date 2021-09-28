from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import get_db
import jwt
import settings
from . import models
from .utils import Hash


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def authenticate(email: str, password: str, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    if not Hash.verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='incorrect password')
    if user.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='User is not active.')
    return user


def generate_token(user):
    user = {
        'id': user.id,
        'email': user.email,
        'is_active': user.is_active,
        'is_admin': user.is_admin
    }
    token = jwt.encode(user, settings.SECRET_KEY)
    return {'access_token': token, 'token_type': 'bearer'}


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, settings.SECRET_KEY,
                         algorithms=[settings.JWT_ALGORITHM])
    user = db.query(models.User).filter(
        models.User.id == payload.get('id')).first()
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password'
        )

    return user


def get_current_user_admin(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.JWT_ALGORITHM])
        user = db.query(models.User).filter(
            models.User.id == payload.get('id')).first()
        if user.is_admin == False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Protected'
            )

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password'
        )

    return user
