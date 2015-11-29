from implugin.sqlalchemy.driver import ModelDriver

from .models import Team


class TeamDriver(ModelDriver):
    model = Team

    def list(self):
        return self.find_all().order_by('name')
