from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from impex.application.models import Base
from impex.teams.models import Team


class Game(Base):
    __tablename__ = 'games'

    STATUS_NOT_STARTED = 0
    STATUS_RUNNING = 1
    STATUS_ENDED = 2

    STATUSES = {
        STATUS_NOT_STARTED: 'Nie rozpoczęto',
        STATUS_RUNNING: 'W trakcie gry',
        STATUS_ENDED: 'Zakończono',
    }

    id = Column(Integer, primary_key=True)
    plaing_at = Column(DateTime())
    priority = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False, default=STATUS_NOT_STARTED)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    left_id = Column(Integer, ForeignKey('teams.id'))
    right_id = Column(Integer, ForeignKey('teams.id'))
    scores = Column(
        JSON,
        default={
            'left': [0, 0, 0, 0],
            'right': [0, 0, 0, 0],
        }
    )

    event = relationship("Event")
    left = relationship(Team, primaryjoin=(left_id == Team.id))
    right = relationship(Team, primaryjoin=(right_id == Team.id))

    def get_sum_for_quart(self, team, quart):
        return sum(self.scores[team][:(quart)])
