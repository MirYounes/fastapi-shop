from fastapi import APIRouter, Depends, status
from accounts import cruds
from accounts.authentication import get_current_user_admin
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from database import get_db
from typing import List, Optional
from accounts import schemas


router = APIRouter(
    tags=["Users Admin"],
    prefix="/admin/users",
    dependencies=[Depends(get_current_user_admin)]
)


@router.get('/', response_model=List[schemas.Users])
async def get_users(db: Session = Depends(get_db), skip: Optional[int] = 0, limit: Optional[int] = 100):
    users = cruds.get_users(db, skip=skip, limit=limit)
    return users


@router.get('/{id}')
async def get_user(id: int, db: Session = Depends(get_db)):
    user = cruds.get_user(db, id)
    return user


@router.delete('/{id}')
async def delete_user(id: int, db: Session = Depends(get_db)):
    cruds.destroy(id, db)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "user deleted"})


@router.put('/{id}')
async def update_user(request: schemas.UpdateUser, id: int, db: Session = Depends(get_db)):
    user = cruds.update(db, request, id)
    return user
