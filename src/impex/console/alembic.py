from alembic import command
from alembic.config import Config
from bael.project.virtualenv import BaseVirtualenv
from baelfire.dependencies import AlwaysRebuild
from baelfire.dependencies import RunBefore

from .base import IniTemplate
from .dependency import MigrationChanged


class AlembicUpgrade(BaseVirtualenv):

    def create_dependecies(self):
        self.add_dependency(RunBefore(IniTemplate()))
        self.add_dependency(MigrationChanged('versions', 'sqlite_db'))

    def build(self):
        alembic_cfg = Config(self.paths['frontendini'])
        command.upgrade(alembic_cfg, "head")
        open(self.paths['sqlite_db'], 'a').close()


class AlembicRevision(BaseVirtualenv):

    def create_dependecies(self):
        self.add_dependency(RunBefore(IniTemplate()))
        self.add_dependency(AlwaysRebuild())

    def build(self):
        alembic_cfg = Config(self.paths['frontendini'])
        command.revision(alembic_cfg)
