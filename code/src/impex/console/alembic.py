import os

from logging import getLogger

from alembic import command
from alembic.config import Config
from baelfire.dependencies import AlwaysTrue
from baelfire.task.process import SubprocessTask

from .base import IniTemplate
from .dependency import MigrationChanged

log = getLogger(__name__)


def touch(fname, mode=0o666, dir_fd=None, **kwargs):
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(fname, flags=flags, mode=mode, dir_fd=dir_fd)) as f:
        os.utime(f.fileno() if os.utime in os.supports_fd else fname,
                 dir_fd=None if os.supports_fd else dir_fd, **kwargs)


class AlembicUpgrade(SubprocessTask):

    def create_dependecies(self):
        self.run_before(IniTemplate())
        self.build_if(MigrationChanged('versions', 'sqlite_db'))

    def build(self):
        log.info("Running migrations...")
        alembic_cfg = Config(self.paths.get('frontendini'))
        command.upgrade(alembic_cfg, "head")
        touch(self.paths.get('sqlite_db'))


class AlembicRevision(SubprocessTask):

    def create_dependecies(self):
        self.run_before(IniTemplate())
        self.build_if(AlwaysTrue())

    def build(self):
        alembic_cfg = Config(self.paths.get('frontendini'))
        message = input('Revision message:')
        command.revision(alembic_cfg, message)
