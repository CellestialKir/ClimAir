from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    password: str
    is_admin: bool = Field(default=False)
    role: str

class UserUpdate(SQLModel):
    id: int = Field(default=None, primary_key=True)
    email: Optional[str]
    role: Optional[str]