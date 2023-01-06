from pydantic import BaseModel

class ItemEdit(BaseModel):
    fakename: str

class ItemBase(BaseModel):
    fakename: str
    ip_id: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True



class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    fakenaam: list[Item] = []


    class Config:
        orm_mode = True



class IpBase(BaseModel):
    ip: str


class IpCreate(IpBase):
    pass


class Ip(IpBase):
    id: int

    class Config:
        orm_mode = True