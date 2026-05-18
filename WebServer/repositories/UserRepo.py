from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, select
from EnvData import postgresql_url
from core.db import engine
from model.User import User, UserUpdate
from core.security import hash_password


def createUser(user:User):

    user.password = hash_password(user.password)

    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)

def updateUser(newUser: UserUpdate):
    with Session(engine) as session:
        oldUser = session.get(User, newUser.id)
        if not oldUser:
            return None

        updateData = newUser.model_dump(exclude_unset=True)

        for key, value in updateData.items():
            setattr(oldUser, key, value)

        session.add(oldUser)
        session.commit()
        session.refresh(oldUser)
        return oldUser

def deletById(id):
    with Session(engine) as session:
        user = session.get(User, id)
        if not user:
            return None
        session.delete(user)
        session.commit()
        return "User deleted successfully"

def getUserById(id):
    with Session(engine) as session:
        user = session.get(User, id)
        if not user:
            return None
        return user


