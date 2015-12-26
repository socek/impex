from implugin.sqlalchemy.driver import ModelDriver

from .models import Group


class GroupDriver(ModelDriver):
    model = Group

    def list(self):
        return self.find_all().order_by(self.model.id)
