from implugin.auth.requestable import AuthRequestable
from implugin.beaker import BeakerRequestable
from implugin.jinja2 import Jinja2Requestable

from impex.auth.models import NotLoggedUser

from .driver import ImpexDriverHolder


class Requestable(
    BeakerRequestable,
    Jinja2Requestable,
    AuthRequestable,
):
    DRIVER_HOLDER_CLS = ImpexDriverHolder
    _not_logged_user_cls = NotLoggedUser
