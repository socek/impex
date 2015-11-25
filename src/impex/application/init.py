from implugin.beaker import BeakerApplication
from implugin.haml import HamlApplication
from implugin.sqlalchemy.application import SqlAlchemyApplication
from implugin.auth.application import AuthApplication
from implugin.fanstatic import FanstaticApplication

from .entryfactory import EntryFactory
from .routing import ImpexRouting


class ImpexApplication(
    HamlApplication,
    BeakerApplication,
    SqlAlchemyApplication,
    FanstaticApplication,
    AuthApplication,
):
    class Config(HamlApplication.Config):
        routing_cls = ImpexRouting

    def __init__(self):
        super().__init__('impex')

    def _get_config_kwargs(self):
        data = super()._get_config_kwargs()
        data['root_factory'] = EntryFactory
        return data

    def _create_config(self):
        super()._create_config()
        if self.settings['debug']:
            self.config.include('pyramid_debugtoolbar')


main = ImpexApplication()
