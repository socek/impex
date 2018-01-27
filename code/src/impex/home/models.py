from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from impex.application.models import Base


class SampleData(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
