from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from database import get_db
from .authentication import authenticate, generate_token, get_current_user
from . import schemas, cruds
from .utils import Hash, send_email, get_from_redis, delete_from_redis


router = APIRouter(
    tags=['accounts'],
    prefix='/accounts'
)


@router.post('/token',)
async def get_token(request: schemas.GetToken, db: Session = Depends(get_db)):
    user = authenticate(email=request.username,
                        password=request.password, db=db)
    token = generate_token(user)
    return token


@router.post('/register', response_model=schemas.ShowUser)
async def user_register(
        background_tasks: BackgroundTasks,
        request: schemas.UserRegister,
        db: Session = Depends(get_db),
):
    user = cruds.get_user_by_email(db, email=request.email)
    if user == None:
        user = cruds.create_user(db, request)
    elif user.is_active == True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user already registered")

    send_email(id=user.id, email=user.email,
               state='register', subject="verify",
               background_tasks=background_tasks)
    return user


@router.post('/register/verify',)
async def user_verify(request: schemas.UserVerfiy, db: Session = Depends(get_db)):
    user = cruds.get_user_by_email(db, email=request.email)
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user does not exist"
        )

    token = get_from_redis(user.id, 'register')
    if token == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="wrong/expired token"
        )

    #cruds.update_user(db , user , is_active=True)
    user.is_active = True
    db.commit()
    delete_from_redis(user.id, 'register')

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message":"your account verfied"})


@router.get('/profile', response_model=schemas.ShowUser)
async def user_detail(user: schemas.ShowUser = Depends(get_current_user)):
    return user


@router.post('/password/change',)
async def change_password(
        request: schemas.UserChangePassword,
        db: Session = Depends(get_db),
        user: schemas.ShowUser = Depends(get_current_user)):

        if not Hash.verify_password(request.old_password , user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="invalid old password"
            )

        if request.new_password1 != request.new_password2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="new password mus equal"
            )

        hashed_password = Hash.get_password_hash(request.new_password1)
        user.hashed_password = hashed_password
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message":"password changed"})          
