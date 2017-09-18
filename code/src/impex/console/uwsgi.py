from bael.project.virtualenv import BaseVirtualenv
from baelfire.dependencies import AlwaysTrue
from baelfire.dependencies.pid import PidIsNotRunning
from baelfire.dependencies.pid import PidIsRunning
from baelfire.error import CommandAborted

from .alembic import AlembicUpgrade


class StartUwsgi(BaseVirtualenv):

    def create_dependecies(self):
        self.run_before(AlembicUpgrade())
        self.build_if(PidIsNotRunning(pid_file_name='uwsgi:pidfile'))

    def build(self):
        try:
            self.popen('{0} --ini-paste {1}'.format(
                self.paths.get('exe:uwsgi'),
                self.paths.get('frontendini')))
        except CommandAborted:
            self.logger.info('Aborted')


class StopUwsgi(BaseVirtualenv):

    def create_dependecies(self):
        self.run_before(AlembicUpgrade())
        self.build_if(PidIsRunning(pid_file_name='uwsgi:pidfile'))

    def build(self):
        try:
            self.popen('{0} --stop {1}'.format(
                self.paths.get('exe:uwsgi'),
                self.paths.get('uwsgi:pidfile')))
        except CommandAborted:
            self.logger.info('Aborted')


class RestartUwsgi(BaseVirtualenv):

    def create_dependecies(self):
        self.run_before(StopUwsgi())
        self.build_if(AlwaysTrue())

    def build(self):
        try:
            self.popen('{0} --stop {1}'.format(
                self.paths.get('exe:uwsgi'),
                self.paths.get('uwsgi:pidfile')))
        except CommandAborted:
            self.logger.info('Aborted')
