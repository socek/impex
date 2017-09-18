from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from impex.application.models import Base


class Order(Base):
    __tablename__ = 'orders'

    STATUS_OPEN = 0
    STATUS_LOCKED = 1
    STATUS_WAITING_FOR_DELIVERY = 2
    STATUS_CLOSED = 3
    STATUS_DELETED = 4

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = DateTime()
    modified_at = DateTime()
    status = Column(Integer, nullable=False, default=STATUS_OPEN)
