from bael.project.virtualenv import BaseVirtualenv
from baelfire.dependencies import AlwaysRebuild
from baelfire.dependencies import RunBefore
from baelfire.error import CommandAborted

from .alembic import AlembicUpgrade


class Serve(BaseVirtualenv):

    def phase_settings(self):
        super().phase_settings()
        # self.paths.set_path('exe:pserve', 'virtualenv:bin', 'pserve')

    def create_dependecies(self):
        self.add_dependency(RunBefore(AlembicUpgrade()))
        self.add_dependency(AlwaysRebuild())

    def build(self):
        try:
            self.popen(
                ['%(exe:pserve)s %(frontendini)s --reload' % self.paths],
            )
        except CommandAborted:
            self.logger.info('Aborted')
