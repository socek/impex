from implugin.beaker import BeakerRequestable
from implugin.sqlalchemy.requestable import SqlalchemyRequestable
from implugin.jinja2 import Jinja2Requestable
from implugin.auth.requestable import AuthRequestable

from .driver import ImpexDriverHolder


class Requestable(
    SqlalchemyRequestable,
    BeakerRequestable,
    Jinja2Requestable,
    AuthRequestable,
):

    def _get_driver_holder_cls(self):
        return ImpexDriverHolder
