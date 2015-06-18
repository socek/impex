from implugin.beaker import BeakerRequestable
from implugin.sqlalchemy.requestable import SqlalchemyRequestable


class Requestable(
    SqlalchemyRequestable,
    BeakerRequestable,
):
    pass
