from implugin.alembic.commands import AlembicCommand
from implugin.alembic.commands import InitDatabase

from .init import ImpexApplication
from .generator import ImpexDataGenerator
from .driver import ImpexDriverHolder


class ImpexAlembicCommand(ImpexApplication, AlembicCommand):
    pass


class ImpexInitDatabase(ImpexApplication, InitDatabase):

    def get_datagenerator(self):
        return ImpexDataGenerator()

    def get_driver(self):
        return ImpexDriverHolder


def alembic():
    ImpexAlembicCommand().run_command()


def initdb():
    ImpexInitDatabase().run_command()
