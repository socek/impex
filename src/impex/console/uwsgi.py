from bael.project.virtualenv import BaseVirtualenv
from baelfire.dependencies import AlwaysRebuild
from baelfire.dependencies import RunBefore
from baelfire.dependencies.pid import PidIsNotRunning
from baelfire.dependencies.pid import PidIsRunning
from baelfire.error import CommandAborted

from .alembic import AlembicUpgrade


class StartUwsgi(BaseVirtualenv):

    def phase_settings(self):
        super().phase_settings()
        # self.paths.set_path('exe:uwsgi', 'virtualenv:bin', 'uwsgi')

    def create_dependecies(self):
        self.add_dependency(RunBefore(AlembicUpgrade()))
        # self.add_dependency(PidIsNotRunning(pid_file_name='uwsgi:pidfile'))

    def build(self):
        try:
            self.popen(
                ['uwsgi --ini-paste %(frontendini)s' % self.paths],
            )
        except CommandAborted:
            self.logger.info('Aborted')


class StopUwsgi(BaseVirtualenv):

    def phase_settings(self):
        super().phase_settings()
        self.paths.set_path('exe:uwsgi', 'virtualenv:bin', 'uwsgi')

    def create_dependecies(self):
        self.add_dependency(RunBefore(AlembicUpgrade()))
        self.add_dependency(PidIsRunning(pid_file_name='uwsgi:pidfile'))

    def build(self):
        try:
            self.popen(
                ['%(exe:uwsgi)s --stop %(uwsgi:pidfile)s' % self.paths],
            )
        except CommandAborted:
            self.logger.info('Aborted')


class RestartUwsgi(BaseVirtualenv):

    def create_dependecies(self):
        self.add_dependency(RunBefore(StopUwsgi()))
        self.add_dependency(AlwaysRebuild())

    def build(self):
        try:
            self.popen(
                ['%(exe:uwsgi)s --ini-paste %(frontendini)s' % self.paths],
            )
        except CommandAborted:
            self.logger.info('Aborted')
