import os

from alembic import command
from alembic.config import Config
from bael.project.virtualenv import BaseVirtualenv
from baelfire.dependencies import AlwaysRebuild
from baelfire.dependencies import RunBefore

from .base import IniTemplate
from .dependency import MigrationChanged


def touch(fname, mode=0o666, dir_fd=None, **kwargs):
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(fname, flags=flags, mode=mode, dir_fd=dir_fd)) as f:
        os.utime(f.fileno() if os.utime in os.supports_fd else fname,
                 dir_fd=None if os.supports_fd else dir_fd, **kwargs)


class AlembicUpgrade(BaseVirtualenv):

    def create_dependecies(self):
        self.add_dependency(RunBefore(IniTemplate()))
        self.add_dependency(MigrationChanged('versions', 'sqlite_db'))

    def build(self):
        alembic_cfg = Config(self.paths['frontendini'])
        command.upgrade(alembic_cfg, "head")
        touch(self.paths['sqlite_db'])


class AlembicRevision(BaseVirtualenv):

    def create_dependecies(self):
        self.add_dependency(RunBefore(IniTemplate()))
        self.add_dependency(AlwaysRebuild())

    def build(self):
        alembic_cfg = Config(self.paths['frontendini'])
        command.revision(alembic_cfg)
