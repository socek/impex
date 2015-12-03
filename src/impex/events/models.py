from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from impex.application.models import Base
from impex.game.models import Game


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    is_visible = Column(Boolean(), default=False)

    games = relationship(Game, order_by=Game.priority)
