from implugin.sqlalchemy.driver import ModelDriver

from .models import Group


class GroupDriver(ModelDriver):
    model = Group
