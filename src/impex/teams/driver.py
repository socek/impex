from sqlalchemy import or_

from implugin.sqlalchemy.driver import ModelDriver

from .models import Team
from impex.events.models import Event
from impex.games.models import Game
from impex.groups.models import Group


class TeamDriver(ModelDriver):
    model = Team

    def list(self):
        return self.find_all().order_by(self.model.name)

    def list_for(self, event_id, group_id):
        return (
            self.list()
            .join(
                Game,
                or_(
                    Game.left_id == self.model.id,
                    Game.right_id == self.model.id,
                )
            )
            .join(Event)
            .join(Group)
            .filter(
                Event.id == event_id,
                Group.id == group_id,
            )
        )
