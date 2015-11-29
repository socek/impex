from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from impex.application.models import Base


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    priority = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    hometown = Column(String)
