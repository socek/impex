from baelfire.dependencies import AlwaysTrue
from baelfire.error import CommandAborted
from baelfire.task.process import SubprocessTask

from .alembic import AlembicUpgrade


class Serve(SubprocessTask):

    def create_dependecies(self):
        self.run_before(AlembicUpgrade())
        self.build_if(AlwaysTrue())

    def build(self):
        try:
            self.popen('{0} {1} --reload'.format(
                self.paths.get('exe:pserve'),
                self.paths.get('frontendini')))
        except CommandAborted:
            self.logger.info('Aborted')
