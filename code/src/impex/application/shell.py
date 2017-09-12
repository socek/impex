from implugin.sqlalchemy.requestable import DatabaseConnection

from impex.application.init import main
from impex.application.driver import ImpexDriverHolder


def setup(env):
    env['main'] = main
    env['db'] = DatabaseConnection(main.settings, main.config.registry).database()
    env['drivers'] = ImpexDriverHolder(lambda: env['db'])
