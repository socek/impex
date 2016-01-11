from sqlalchemy import and_
from sqlalchemy import or_

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

    def list_except(self, event_id, game_id, group_id):
        return (
            self.list_for_group(event_id, group_id)
            .filter(self.model.id != game_id)
        )

    def list_for_group(self, event_id, group_id):
        return self.list(event_id).filter(self.model.group_id == group_id)

    def get_next_avalible_priority(self, event_id):
        return self.list(event_id).count() + 1

    def find_by_priority(self, event_id, priority):
        return (
            self.list(event_id)
            .filter(self.model.priority >= priority)
        )

    def increment_priorities_by(self, event_id, priority, game):
        elements = self.list(event_id).all()
        elements.remove(game)
        elements.insert(priority - 1, game)
        for index, game in enumerate(elements):
            game.priority = index + 1
        self.database().flush()

    def is_doubled(self, event_id, left_id, right_id, except_id=None):
        query = (
            self.find_all()
            .filter(self.model.event_id == event_id)
            .filter(
                or_(
                    and_(
                        self.model.left_id == left_id,
                        self.model.right_id == right_id,
                    ),
                    and_(
                        self.model.left_id == right_id,
                        self.model.right_id == left_id,
                    )
                )
            )
        )
        if except_id:
            query = query.filter(self.model.id != except_id)
        return query.count() > 0
