from implugin.beaker import BeakerRequestable
from implugin.jinja2 import Jinja2Requestable
from implugin.auth.requestable import AuthRequestable

from .driver import ImpexDriverHolder


class Requestable(
    BeakerRequestable,
    Jinja2Requestable,
    AuthRequestable,
):
    DRIVER_HOLDER_CLS = ImpexDriverHolder
