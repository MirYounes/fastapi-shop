from pydantic import BaseModel


class GetToken(BaseModel):
    username: str
    password: str


class UserRegister(BaseModel):
    full_name: str
    username: str
    email: str
    password: str


class UserVerfiy(BaseModel):
    email: str
    token: str


class ShowUser(BaseModel):
    id : int
    full_name: str
    username: str
    email: str

    class Config:
        orm_mode = True


class UserChangePassword(BaseModel):
    old_password : str 
    new_password1 : str 
    new_password2 : str


class Users(BaseModel):
    id : int 
    username : str 
    email : str
    is_active : bool
    is_admin : bool

    class Config :
        orm_mode = True


class UpdateUser(BaseModel):
    username : str = None
    email : str = None
    full_name : str = None
    is_active : bool = None
    is_admin : bool  = None  