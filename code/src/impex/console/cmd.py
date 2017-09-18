from argparse import ArgumentParser
from logging import getLogger

from baelfire.application.application import Application
from baelfire.application.commands.graph.graph import Graph

from impex.console.alembic import AlembicRevision
from impex.console.alembic import AlembicUpgrade
from impex.console.core import ImpexCore
from impex.console.serve import Serve
from impex.console.uwsgi import RestartUwsgi
from impex.console.uwsgi import StartUwsgi
from impex.console.uwsgi import StopUwsgi

log = getLogger(__name__)


class WeWalletApplication(Application):

    tasks = {
        'serve': Serve,
        'alembic-upgrade': AlembicUpgrade,
        'alembic-revision': AlembicRevision,
        'uwsgi_start': StartUwsgi,
        'uwsgi_stop': StopUwsgi,
        'uwsgi_restart': RestartUwsgi,
    }

    def create_parser(self):
        self.parser = ArgumentParser()
        self._add_task_group()
        self._add_logging_group()

    def _add_task_group(self):
        tasks = self.parser.add_argument_group(
            'Tasks',
            'Project related options',
        )

        group = tasks.add_mutually_exclusive_group()
        group.add_argument(
            '-d',
            '--develop',
            dest='task',
            help='Download requiretments.',
            action='store_const',
            const='develop',
        )
        group.add_argument(
            '-s',
            '--serve',
            dest='task',
            help='Start development server.',
            action='store_const',
            const='serve',
        )
        group.add_argument(
            '-u',
            '--alembic-upgrade',
            dest='task',
            help='Run migrations.',
            action='store_const',
            const='alembic-upgrade',
        )
        group.add_argument(
            '-r',
            '--alembic-revision',
            dest='task',
            help='Create migration.',
            action='store_const',
            const='alembic-revision',
        )
        group.add_argument(
            '-w',
            '--uwsgi-start',
            dest='task',
            help='Start uwsgi',
            action='store_const',
            const='uwsgi_start',
        )
        group.add_argument(
            '-n',
            '--uwsgi-stop',
            dest='task',
            help='Stop uwsgi',
            action='store_const',
            const='uwsgi_stop',
        )
        group.add_argument(
            '-e',
            '--uwsgi-restart',
            dest='task',
            help='Restart uwsgi',
            action='store_const',
            const='uwsgi_restart',
        )

        tasks.add_argument(
            '-g',
            '--graph',
            dest='graph',
            help='Draw task dependency graph.',
            action="store_true",
        )

    def run_command_or_print_help(self, args):
        if args.task:
            task = self._get_task(args)
            try:
                try:
                    task.run()
                finally:
                    report_path = task.save_report()
            except:
                log.error('Error in %s' % (report_path,))
                raise
            if args.graph:
                Graph(report_path).render()
        else:
            self.parser.print_help()

    def _get_task(self, args):
        return self.tasks[args.task](ImpexCore())


def run():
    WeWalletApplication().run()
