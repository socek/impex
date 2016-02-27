from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from impex.application.models import Base


class SliderEvent(Base):
    __tablename__ = 'slider_events'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(String)
    when_created = Column(DateTime(), default=datetime.now)


class TabData(Base):
    __tablename__ = 'tab_data'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_visible = Column(Boolean, default=True)
