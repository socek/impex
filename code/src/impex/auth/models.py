from sqlalchemy import Boolean
from sqlalchemy import Column

from implugin.auth.models import BaseUser as VeryBaseUser
from implugin.auth.models import NotLoggedUser as BaseNotLoggedUser

from impex.application.models import Base


class BaseUser(VeryBaseUser):
    is_admin = Column(Boolean(), default=False)


class NotLoggedUser(BaseUser, BaseNotLoggedUser):
    is_admin = False


class User(BaseUser, Base):
    __tablename__ = 'users'
