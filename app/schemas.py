from pydantic import BaseModel

# Схемы данных

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


class Message(BaseModel):
    sender_id: int
    recipient_id: int
    content: str

    class Config:
        orm_mode = True