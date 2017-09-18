from implugin.auth.application import AuthApplication
from implugin.beaker import BeakerApplication
from implugin.fanstatic import FanstaticApplication
from implugin.haml import HamlApplication
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from implugin.sqlalchemy.application import SqlAlchemyApplication
from morfdict import Factory


from .entryfactory import EntryFactory
from .routing import ImpexRouting


class SettingsFactory(object):
    """
    This class will generate settings for different endpoints.
    """
    ENDPOINTS = {
        'uwsgi': [('local', False)],
        'tests': [('tests', False)],
        'shell': [('shell', False), ('local_shell', False)],
        'command': [('command', False), ('local', False)],
    }

    def __init__(self, module, settings=None, paths=None):
        self.module = module
        self.settings = settings or {}
        self.paths = paths or {}

    def get_for(self, endpoint):
        files = self.ENDPOINTS[endpoint]
        return self._generate_settings(files)

    def _generate_settings(self, files=None):
        files = files or []
        factory = Factory(self.module)
        settings, paths = factory.make_settings(
            settings=self.settings,
            additional_modules=files,
        )
        settings['paths'] = paths
        return settings, paths


class ImpexApplication(
    HamlApplication,
    BeakerApplication,
    # SqlAlchemyApplication,
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

    def _generate_settings(
        self,
        settings,
        endpoint,
        factorycls=SettingsFactory,
    ):
        super()._generate_settings(settings, endpoint, factorycls)

    def _generate_registry(self, registry):
        super()._generate_registry(registry)
        engine = create_engine(self.settings['dburl'])
        registry['db_engine'] = engine
        registry['db'] = sessionmaker(bind=engine)()


main = ImpexApplication()
