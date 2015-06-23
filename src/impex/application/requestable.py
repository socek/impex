from implugin.beaker import BeakerRequestable
from implugin.sqlalchemy.requestable import SqlalchemyRequestable

from .driver import ImpexDriverHolder


class Requestable(
    SqlalchemyRequestable,
    BeakerRequestable,
):

    def _get_driver_holder_cls(self):
        return ImpexDriverHolder
