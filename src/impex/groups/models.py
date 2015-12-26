from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from impex.application.models import Base


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def games_len(self):
        return len(self.games)
