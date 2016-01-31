from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from impex.application.models import Base


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ladder = Column(Boolean, nullable=False, default=False)
    games = relationship("Game", order_by='Game.priority')

    def games_len(self):
        return len(self.games)
