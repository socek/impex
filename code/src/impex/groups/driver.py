from sqlalchemy import func

from implugin.sqlalchemy.driver import ModelDriver

from impex.events.models import Event
from impex.games.models import Game

from .models import Group


class GroupDriver(ModelDriver):
    model = Group

    def list(self):
        return self.find_all().order_by(self.model.id)

    def list_not_empty(self, event_id):
        return (
            self.list()
            .outerjoin(Game)
            .outerjoin(Event)
            .filter(Event.id == event_id)
            .group_by(Group.id)
            .having(
                func.count(Game.id) > 0
            )
        )
