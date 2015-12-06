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

    def get_next_avalible_priority(self, event_id):
        return self.list(event_id).count() + 1

    def find_by_priority(self, event_id, priority):
        return (
            self.list(event_id)
            .filter(self.model.priority >= priority)
        )
