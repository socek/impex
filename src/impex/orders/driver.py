from implugin.sqlalchemy.driver import ModelDriver

from .models import Order


class OrderDriver(ModelDriver):
    model = Order
