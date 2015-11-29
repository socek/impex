from implugin.sqlalchemy.driver import ModelDriver

from .models import Team


class TeamDriver(ModelDriver):
    model = Team
