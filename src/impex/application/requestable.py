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

    def add_event(self, name, value):
        self.drivers.slider_event.create(
            name=name,
            value=value,
        )
        self.database().commit()

    def refresh_scores(self):
        self.add_event('refresh', 'scores')
        self.add_event('refresh', 'high_scores')
        self.add_event('refresh', 'group_a')
        self.add_event('refresh', 'group_b')
        self.add_event('refresh', 'finals')
