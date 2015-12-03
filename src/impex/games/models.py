from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from impex.application.models import Base


class Game(Base):
    __tablename__ = 'games'

    STATUS_NOT_STARTED = 0
    STATUS_RUNNING = 1
    STATUS_ENDED = 2

    id = Column(Integer, primary_key=True)
    plaing_at = DateTime()
    priority = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False, default=STATUS_NOT_STARTED)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    left_id = Column(Integer, ForeignKey('teams.id'))
    right_id = Column(Integer, ForeignKey('teams.id'))
    scores = Column(JSON)

    event = relationship("Event")
