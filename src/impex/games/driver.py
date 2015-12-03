from implugin.sqlalchemy.driver import ModelDriver

from .models import Game


class GameDriver(ModelDriver):
    model = Game

    def list(self, event_id):
        return (
            self.find_all()
            .filter(self.model.event_id == event_id)
            .order_by(self.model.priority)
        )
